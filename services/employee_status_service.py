"""
สถานะพนักงาน / เวลาทำงาน / การลา / การขาดงานกะทันหัน

status_employee (seed คงที่จาก migration):
  1=available  2=working  3=break  4=leave  5=absent  6=off
"""

from services.db import get_conn
from services.timeutil import bangkok_today, to_date

STATUS_AVAILABLE = 1
STATUS_WORKING = 2
STATUS_BREAK = 3
STATUS_LEAVE = 4
STATUS_ABSENT = 5
STATUS_OFF = 6

# สถานะที่ต้องตั้งผ่าน endpoint เฉพาะ (ลา/ขาดงาน) เท่านั้น ห้ามตั้งตรงผ่าน
# set_employee_current_status เพื่อให้ employee_absence เป็นแหล่งข้อมูลจริงเสมอ
_RESTRICTED_STATUSES = {STATUS_LEAVE, STATUS_ABSENT}


# ============================================================
#   GET EMPLOYEE STATUS TODAY (สำหรับหน้าจอ "สถานะพนักงานวันนี้")
# ============================================================
def get_employee_status_today(store_id: int, only_employee_id: int = None):
    conn = get_conn()
    cur = conn.cursor()

    today = bangkok_today()

    sql = """
        SELECT
            e.employee_id,
            e.fullname,
            e.position,
            e.current_status_id,
            se.status_employee_name,
            EXISTS(
                SELECT 1 FROM employee_absence ea
                WHERE ea.employee_id = e.employee_id AND ea.absence_date = %(today)s
                  AND ea.status = 'ACTIVE' AND ea.absence_type = 'LEAVE'
            ) AS on_leave_today,
            EXISTS(
                SELECT 1 FROM employee_absence ea
                WHERE ea.employee_id = e.employee_id AND ea.absence_date = %(today)s
                  AND ea.status = 'ACTIVE' AND ea.absence_type = 'ABSENT'
            ) AS on_absent_today
        FROM employee e
        LEFT JOIN status_employee se ON se.status_employee_id = e.current_status_id
        WHERE e.store_id = %(store_id)s AND e.deleted_at IS NULL
    """
    params = {"store_id": store_id, "today": today}

    if only_employee_id is not None:
        sql += " AND e.employee_id = %(only_employee_id)s"
        params["only_employee_id"] = only_employee_id

    sql += " ORDER BY e.employee_id"

    cur.execute(sql, params)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#   SET CURRENT (LIVE) STATUS -- Available / Working / Break / Off เท่านั้น
# ============================================================
def set_employee_current_status(employee_id: int, status_employee_id: int, changed_by=None):
    if status_employee_id in _RESTRICTED_STATUSES:
        raise ValueError("ต้องตั้งค่าสถานะลา/ขาดงานผ่านฟังก์ชันเฉพาะเท่านั้น")

    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "UPDATE employee SET current_status_id = %s WHERE employee_id = %s AND deleted_at IS NULL",
        (status_employee_id, employee_id)
    )
    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#   WORK HOURS (ตารางเวลาทำงานรายสัปดาห์)
# ============================================================
def get_employee_work_hours(employee_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            work_hours_id, day_of_week,
            TIME_FORMAT(start_time, '%%H:%%i') AS start_time,
            TIME_FORMAT(end_time, '%%H:%%i') AS end_time,
            is_working
        FROM employee_work_hours
        WHERE employee_id = %s
        ORDER BY day_of_week
    """, (employee_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def set_employee_work_hours(employee_id: int, hours: list):
    for h in hours or []:
        dow = h.get("day_of_week")
        if dow is None or not (1 <= int(dow) <= 7):
            raise ValueError("day_of_week ต้องอยู่ระหว่าง 1-7")
        if h.get("is_working", True) and (not h.get("start_time") or not h.get("end_time")):
            raise ValueError("ต้องระบุเวลาเริ่ม/สิ้นสุดสำหรับวันที่ทำงาน")

    conn = get_conn()
    cur = conn.cursor()

    try:
        conn.begin()

        cur.execute("DELETE FROM employee_work_hours WHERE employee_id = %s", (employee_id,))

        if hours:
            cur.executemany("""
                INSERT INTO employee_work_hours
                    (employee_id, day_of_week, start_time, end_time, is_working)
                VALUES (%s, %s, %s, %s, %s)
            """, [
                (employee_id, h["day_of_week"], h.get("start_time") or "00:00:00",
                 h.get("end_time") or "23:59:59", 1 if h.get("is_working", True) else 0)
                for h in hours
            ])

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#   LEAVE (ลาล่วงหน้า / ครึ่งวัน / เต็มวัน / กะทันหัน)
# ============================================================
def create_leave(employee_id: int, leave_scope: str, absence_date, start_time=None,
                  end_time=None, reason=None, created_by=None):
    if leave_scope not in ("FULL_DAY", "HALF_DAY"):
        raise ValueError("leave_scope ต้องเป็น FULL_DAY หรือ HALF_DAY")
    if leave_scope == "HALF_DAY" and (not start_time or not end_time):
        raise ValueError("ลาครึ่งวันต้องระบุเวลาเริ่ม/สิ้นสุด")

    absence_date = to_date(absence_date)
    conn = get_conn()
    cur = conn.cursor()

    try:
        conn.begin()

        # สถานะเริ่มต้นเป็น PENDING เสมอ -- ยังไม่มีผลใด ๆ ต่อการจองจนกว่าจะถูก
        # อนุมัติผ่าน approve_leave() ก่อน (ต่างจาก ABSENT ที่มีผลทันที)
        cur.execute("""
            INSERT INTO employee_absence
                (employee_id, absence_type, leave_scope, absence_date,
                 start_time, end_time, reason, status, created_by)
            VALUES (%s, 'LEAVE', %s, %s, %s, %s, %s, 'PENDING', %s)
        """, (
            employee_id,
            leave_scope,
            absence_date,
            start_time if leave_scope == "HALF_DAY" else None,
            end_time if leave_scope == "HALF_DAY" else None,
            reason,
            created_by,
        ))
        absence_id = cur.lastrowid

        conn.commit()
        return absence_id

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#   อนุมัติ/ปฏิเสธคำขอลา (เฉพาะแถวที่ยังเป็น PENDING เท่านั้น)
# ============================================================
def approve_leave(absence_id: int, approved_by=None):
    conn = get_conn()
    cur = conn.cursor()

    try:
        conn.begin()

        cur.execute(
            "SELECT employee_id, absence_date FROM employee_absence "
            "WHERE absence_id = %s AND absence_type = 'LEAVE' AND status = 'PENDING' FOR UPDATE",
            (absence_id,)
        )
        row = cur.fetchone()
        if not row:
            conn.rollback()
            return False

        cur.execute(
            "UPDATE employee_absence SET status = 'ACTIVE', created_by = COALESCE(%s, created_by) "
            "WHERE absence_id = %s",
            (approved_by, absence_id)
        )

        if row["absence_date"] == bangkok_today():
            cur.execute(
                "UPDATE employee SET current_status_id = %s WHERE employee_id = %s",
                (STATUS_LEAVE, row["employee_id"])
            )

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


def reject_leave(absence_id: int, rejected_by=None):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute(
        "UPDATE employee_absence SET status = 'REJECTED', created_by = COALESCE(%s, created_by) "
        "WHERE absence_id = %s AND absence_type = 'LEAVE' AND status = 'PENDING'",
        (rejected_by, absence_id)
    )
    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#   สถานะลา/ขาดงานของพนักงานทุกคนในร้าน สำหรับ "วันที่ใดวันหนึ่ง" (ไม่จำกัด
#   แค่วันนี้) -- ใช้แสดง badge "ลา" บนหน้าจองของลูกค้าทันทีที่เลือกวันที่
#   โดยไม่ต้องกดเปิด dropdown เวลาก่อน
# ============================================================
def get_employee_day_status(store_id: int, target_date, only_employee_id: int = None):
    target_date = to_date(target_date)

    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT
            e.employee_id,
            EXISTS(
                SELECT 1 FROM employee_absence ea
                WHERE ea.employee_id = e.employee_id AND ea.absence_date = %(date)s
                  AND ea.status = 'ACTIVE' AND ea.absence_type = 'LEAVE'
            ) AS on_leave,
            EXISTS(
                SELECT 1 FROM employee_absence ea
                WHERE ea.employee_id = e.employee_id AND ea.absence_date = %(date)s
                  AND ea.status = 'ACTIVE' AND ea.absence_type = 'ABSENT'
            ) AS on_absent
        FROM employee e
        WHERE e.store_id = %(store_id)s AND e.deleted_at IS NULL
    """
    params = {"store_id": store_id, "date": target_date}

    if only_employee_id is not None:
        sql += " AND e.employee_id = %(only_employee_id)s"
        params["only_employee_id"] = only_employee_id

    cur.execute(sql, params)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_pending_leaves(store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            ea.absence_id, ea.employee_id, e.fullname, ea.leave_scope, ea.absence_date,
            TIME_FORMAT(ea.start_time, '%%H:%%i') AS start_time,
            TIME_FORMAT(ea.end_time, '%%H:%%i') AS end_time,
            ea.reason, ea.requested_at
        FROM employee_absence ea
        JOIN employee e ON ea.employee_id = e.employee_id
        WHERE e.store_id = %s AND ea.absence_type = 'LEAVE' AND ea.status = 'PENDING'
        ORDER BY ea.absence_date
    """, (store_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_employee_leaves(employee_id: int, date_from=None, date_to=None):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT
            absence_id, employee_id, absence_type, leave_scope, absence_date,
            TIME_FORMAT(start_time, '%%H:%%i') AS start_time,
            TIME_FORMAT(end_time, '%%H:%%i') AS end_time,
            reason, status, requested_at, created_by, created_at, updated_at
        FROM employee_absence
        WHERE employee_id = %s AND absence_type = 'LEAVE'
    """
    params = [employee_id]

    if date_from:
        sql += " AND absence_date >= %s"
        params.append(date_from)
    if date_to:
        sql += " AND absence_date <= %s"
        params.append(date_to)

    sql += " ORDER BY absence_date DESC"

    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def cancel_leave(absence_id: int):
    conn = get_conn()
    cur = conn.cursor()

    try:
        conn.begin()

        cur.execute(
            "SELECT employee_id, absence_date, status FROM employee_absence "
            "WHERE absence_id = %s AND absence_type = 'LEAVE' AND status IN ('PENDING', 'ACTIVE') FOR UPDATE",
            (absence_id,)
        )
        row = cur.fetchone()
        if not row:
            conn.rollback()
            return False

        was_active = row["status"] == "ACTIVE"

        cur.execute(
            "UPDATE employee_absence SET status = 'CANCELLED' WHERE absence_id = %s",
            (absence_id,)
        )

        if was_active and row["absence_date"] == bangkok_today():
            cur.execute("""
                SELECT COUNT(*) AS cnt FROM employee_absence
                WHERE employee_id = %s AND absence_date = %s AND status = 'ACTIVE'
            """, (row["employee_id"], row["absence_date"]))
            remaining = cur.fetchone()["cnt"]
            if remaining == 0:
                cur.execute(
                    "UPDATE employee SET current_status_id = %s WHERE employee_id = %s",
                    (STATUS_AVAILABLE, row["employee_id"])
                )

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#   SUDDEN ABSENCE (จุดเริ่มต้น flow "ช่างไม่มาทำงานกะทันหัน")
# ============================================================
def set_employee_absent(employee_id: int, absence_date, reason=None, created_by=None):
    from services.booking_service import get_affected_bookings_for_employee

    absence_date = to_date(absence_date)

    conn = get_conn()
    cur = conn.cursor()

    try:
        conn.begin()

        cur.execute("""
            SELECT absence_id FROM employee_absence
            WHERE employee_id = %s AND absence_date = %s
              AND absence_type = 'ABSENT' AND status = 'ACTIVE'
            FOR UPDATE
        """, (employee_id, absence_date))
        if cur.fetchone():
            conn.rollback()
            raise ValueError("พนักงานคนนี้ถูกบันทึกว่าขาดงานในวันนี้แล้ว")

        cur.execute("""
            INSERT INTO employee_absence
                (employee_id, absence_type, leave_scope, absence_date, reason, status, created_by)
            VALUES (%s, 'ABSENT', NULL, %s, %s, 'ACTIVE', %s)
        """, (employee_id, absence_date, reason, created_by))

        if absence_date == bangkok_today():
            cur.execute(
                "UPDATE employee SET current_status_id = %s WHERE employee_id = %s",
                (STATUS_ABSENT, employee_id)
            )

        conn.commit()

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()

    affected = get_affected_bookings_for_employee(employee_id, absence_date)
    return {
        "affected_count": len(affected),
        "affected_bookings": affected,
    }
