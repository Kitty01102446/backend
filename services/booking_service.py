from services.db import get_conn
from services.timeutil import bangkok_today, bangkok_time_now, to_date
import pymysql



# ============================================================
#                     SELECT ALL BOOKINGS
# ============================================================
def get_all_booking():
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT
            booking_id,
            booking_date,
            TIME_FORMAT(booking_time, '%%H:%%i') AS booking_time,
            user_id,
            employee_id,
            store_id,
            type_booking_id,
            status_booking_id,
            total_price,
            total_minutes,
            created_at,
            updated_at
        FROM bookings
        WHERE deleted_at IS NULL
        ORDER BY booking_date, booking_time
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT BOOKING BY ID
# ============================================================
def get_booking_by_id(bid: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT
            booking_id,
            booking_date,
            TIME_FORMAT(booking_time, '%%H:%%i') AS booking_time,
            user_id,
            employee_id,
            store_id,
            customer_name,
            customer_phone,
            customer_line,
            customer_email,
            customer_note,
            total_price,
            total_minutes,
            type_booking_id,
            status_booking_id,
            created_at,
            updated_at
        FROM bookings
        WHERE booking_id = %s
          AND deleted_at IS NULL
    """, (bid,))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT BOOKING
#
#   - employee_id ระบุมาชัดเจน (CUSTOMER_CHOICE): ตรวจสอบ eligibility เต็มรูปแบบ
#     (ทักษะ/ลา/ขาดงาน/เวลาทำงาน/คิวชน) ก่อนยืนยัน ถ้าไม่ผ่านให้ reject ทันที
#     (ห้ามเงียบ ๆ สลับช่างให้เอง)
#   - employee_id ว่าง (SYSTEM_PICK / "System Match"): สุ่มจาก Eligible Staff
#     เท่านั้น ถ้าไม่มีใครว่างจริง fallback เป็น employee_id = NULL เหมือนพฤติกรรม
#     เดิมของระบบ (แถวเก่าที่ employee_id เป็น NULL อยู่แล้วในฐานข้อมูล)
#   - ทำงานภายใต้ transaction + row lock เพื่อกันปัญหาจองซ้ำเวลาเดียวกัน (race
#     condition) และตรวจคิวชนแบบช่วงเวลาทับซ้อนจริง ไม่ใช่ตรงเป๊ะแบบเดิม
# ============================================================
def insert_booking(data: dict):
    from services.booking_eligibility_service import (
        get_eligible_employees,
        has_time_conflict,
        acquire_employee_date_lock,
        pick_and_lock_employee,
    )

    booking_date = data["booking_date"]
    booking_time = data["booking_time"]
    store_id = data["store_id"]
    total_minutes = data.get("total_minutes")
    services = data.get("services") or []
    service_ids = [s["service_id"] for s in services if s.get("service_id") is not None]
    requested_employee_id = data.get("employee_id")

    conn = get_conn()
    cur = conn.cursor()

    try:
        conn.begin()

        final_employee_id = None
        assignment_type = None

        if requested_employee_id:
            assignment_type = "CUSTOMER_CHOICE"

            acquire_employee_date_lock(cur, requested_employee_id, booking_date)

            eligible = get_eligible_employees(
                store_id, booking_date, booking_time, total_minutes, service_ids, cur=cur
            )
            if not any(e["employee_id"] == requested_employee_id for e in eligible):
                if has_time_conflict(requested_employee_id, booking_date, booking_time,
                                      total_minutes, cur=cur):
                    raise Exception("พนักงานมีคิวในเวลานี้แล้ว")
                raise Exception("พนักงานไม่สามารถให้บริการในช่วงเวลานี้")

            final_employee_id = requested_employee_id

        else:
            assignment_type = "SYSTEM_PICK"
            final_employee_id = pick_and_lock_employee(
                cur, store_id, booking_date, booking_time, total_minutes, service_ids
            )
            # ถ้าไม่มีช่างว่างจริง final_employee_id จะเป็น None -> บันทึกแบบยังไม่ระบุช่าง
            # (พฤติกรรมเดิมของระบบที่มีอยู่แล้ว ไม่ใช่สถานะผิดพลาดใหม่)

        sql = """
            INSERT INTO bookings (
              booking_date, booking_time,
              user_id, employee_id, assignment_type, store_id,
              customer_name, customer_phone,
              customer_line, customer_email, customer_note,
              total_price, total_minutes,
              type_booking_id, status_booking_id,
              created_at, updated_at
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())
        """

        cur.execute(sql, (
            booking_date,
            booking_time,
            data["user_id"],
            final_employee_id,
            assignment_type,
            store_id,

            data["customer"]["name"],
            data["customer"]["phone"],
            data["customer"].get("line"),
            data["customer"].get("email"),
            data["customer"].get("note"),

            data["total_price"],
            total_minutes,

            data["type_booking_id"],
            data["status_booking_id"],
        ))

        booking_id = cur.lastrowid

        if services:
            cur.executemany("""
                INSERT INTO booking_services
                (booking_id, service_id, service_name, service_price, service_minutes)
                VALUES (%s,%s,%s,%s,%s)
            """, [
                (booking_id, s["service_id"], s["name"], s["price"], s["minutes"])
                for s in services
            ])

        conn.commit()
        return booking_id

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#                      UPDATE BOOKING
#
#   ถ้ามีการเปลี่ยน employee_id / booking_date / booking_time ให้ตรวจสอบ
#   eligibility + คิวชน (ช่วงเวลาทับซ้อนจริง) ใหม่เสมอ ก่อนแก้ไขจริง
# ============================================================
def update_booking(bid: int, data: dict):
    from services.booking_eligibility_service import (
        get_eligible_employees,
        has_time_conflict,
        acquire_employee_date_lock,
    )

    allow_fields = [
        "booking_date",
        "booking_time",
        "employee_id",
        "store_id",
        "type_booking_id",
        "status_booking_id",
    ]

    fields = []
    values = []

    for field in allow_fields:
        if field in data:
            fields.append(f"{field}=%s")
            values.append(data[field])

    if not fields:
        return False

    needs_validation = any(f in data for f in ("employee_id", "booking_date", "booking_time"))

    conn = get_conn()
    cur = conn.cursor()

    try:
        if needs_validation:
            conn.begin()

            cur.execute("""
                SELECT booking_date, booking_time, employee_id, store_id, total_minutes
                FROM bookings
                WHERE booking_id = %s AND deleted_at IS NULL
                FOR UPDATE
            """, (bid,))
            current = cur.fetchone()
            if not current:
                conn.rollback()
                return False

            new_employee_id = data.get("employee_id", current["employee_id"])
            new_date = data.get("booking_date", current["booking_date"])
            new_time = data.get("booking_time", current["booking_time"])
            total_minutes = current["total_minutes"]

            if new_employee_id:
                acquire_employee_date_lock(cur, new_employee_id, new_date)

                cur.execute("SELECT service_id FROM booking_services WHERE booking_id=%s", (bid,))
                service_ids = [r["service_id"] for r in cur.fetchall()]

                eligible = get_eligible_employees(
                    data.get("store_id", current["store_id"]), new_date, new_time,
                    total_minutes, service_ids, exclude_booking_id=bid, cur=cur
                )
                if not any(e["employee_id"] == new_employee_id for e in eligible):
                    if has_time_conflict(new_employee_id, new_date, new_time, total_minutes,
                                          exclude_booking_id=bid, cur=cur):
                        raise Exception("พนักงานมีคิวในเวลานี้แล้ว")
                    raise Exception("พนักงานไม่สามารถให้บริการในช่วงเวลานี้")

        sql = f"""
            UPDATE bookings
            SET {', '.join(fields)},
                updated_at = NOW()
            WHERE booking_id = %s
              AND deleted_at IS NULL
        """

        values.append(bid)

        cur.execute(sql, tuple(values))
        conn.commit()

        updated = cur.rowcount > 0
        return updated

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#                  DELETE BOOKING (SOFT DELETE)
# ============================================================
def delete_booking(bid: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE bookings
        SET deleted_at = NOW()
        WHERE booking_id = %s
    """, (bid,))

    conn.commit()
    deleted = cur.rowcount > 0
    cur.close()
    conn.close()
    return deleted


# ============================================================
#               INSERT BOOKING SERVICES
# ============================================================
def insert_booking_services(booking_id: int, services: list):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO booking_services
        (booking_id, service_id, service_name, service_price, service_minutes)
        VALUES (%s,%s,%s,%s,%s)
    """

    for s in services:
        cur.execute(sql, (
            booking_id,
            s["service_id"],
            s["name"],
            s["price"],
            s["minutes"]
        ))

    conn.commit()
    cur.close()
    conn.close()


# ============================================================
#     SELECT BOOKING + SERVICES (DETAIL)
# ============================================================
def get_booking_with_services(bid: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT
            b.booking_id,
            b.booking_date,
            DATE_FORMAT(b.booking_date, '%%Y-%%m-%%d') AS booking_date_iso,
            TIME_FORMAT(b.booking_time, '%%H:%%i') AS booking_time,
            b.employee_id,

            b.customer_name,
            b.customer_phone,
            b.customer_email,
            b.customer_note,

            bs.service_id,
            bs.service_name,
            bs.service_price,
            bs.service_minutes,

            b.total_price,
            b.total_minutes,
            b.created_at,

            b.status_booking_id,
            sb.status_booking_name,
            b.cancellation_reason,
            b.cancelled_by,
            b.cancelled_at,

            e.fullname AS employee_name,

            s.store_id,
            s.store_name,
            s.phone AS store_phone,
            s.image AS store_image,
            s.address AS store_address
        FROM bookings b
        JOIN booking_services bs ON b.booking_id = bs.booking_id
        LEFT JOIN status_booking sb ON b.status_booking_id = sb.status_booking_id
        LEFT JOIN employee e ON b.employee_id = e.employee_id
        LEFT JOIN store s ON b.store_id = s.store_id
        WHERE b.booking_id = %s
          AND b.deleted_at IS NULL
    """, (bid,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#     SELECT BOOKINGS BY USER ID (ดึงการจองของผู้ใช้จาก user_id)
# ============================================================
def get_user_bookings(user_id: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("""
            SELECT
                b.booking_id,
                DATE_FORMAT(b.booking_date, '%%Y-%%m-%%d') AS booking_date,
                TIME_FORMAT(b.booking_time, '%%H:%%i') AS booking_time,

                s.store_name,

                b.status_booking_id,
                sb.status_booking_name,
                b.cancelled_by,
                b.total_price,

                (SELECT GROUP_CONCAT(service_name SEPARATOR ', ')
                 FROM booking_services bs
                 WHERE bs.booking_id = b.booking_id) AS svc

            FROM bookings b

            LEFT JOIN store s
                ON b.store_id = s.store_id

            LEFT JOIN status_booking sb
                ON b.status_booking_id = sb.status_booking_id

            WHERE b.user_id = %s
              AND b.deleted_at IS NULL

            ORDER BY b.created_at DESC
        """, (user_id,))

        rows = cur.fetchall()
        return rows

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        cur.close()
        conn.close()

# ============================================================
#     SELECT BOOKINGS BY STORE ID
# ============================================================
def get_store_bookings(store_id: int, only_employee_id=None):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        SELECT
            b.booking_id,
            DATE_FORMAT(b.booking_date, '%%d/%%m/%%Y') AS booking_date,
            TIME_FORMAT(b.booking_time, '%%H:%%i') AS booking_time,
            b.customer_name,
            b.customer_phone,
            b.user_id,
            b.employee_id,
            b.total_price,
            b.status_booking_id,
            sb.status_booking_name,
            b.cancelled_by,
            e.fullname AS employee_name,

            GROUP_CONCAT(bs.service_name SEPARATOR ', ') AS services

        FROM bookings b
        LEFT JOIN employee e ON b.employee_id = e.employee_id
        LEFT JOIN status_booking sb ON b.status_booking_id = sb.status_booking_id
        LEFT JOIN booking_services bs ON b.booking_id = bs.booking_id

        WHERE b.store_id = %s
          AND b.deleted_at IS NULL
    """
    params = [store_id]

    if only_employee_id is not None:
        sql += " AND b.employee_id = %s"
        params.append(only_employee_id)

    sql += " GROUP BY b.booking_id ORDER BY b.created_at DESC"

    cur.execute(sql, tuple(params))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows



def update_booking_status_service(booking_id, status_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE bookings
        SET status_booking_id = %s,
            updated_at = NOW()
        WHERE booking_id = %s
          AND deleted_at IS NULL
    """, (status_id, booking_id))

    conn.commit()

    updated = cur.rowcount > 0

    cur.close()
    conn.close()

    return updated


# ============================================================
#   บันทึกข้อมูลการยกเลิกโดยร้าน (ใช้ร่วมกับ update_booking_status_service เดิม
#   ตอน status_booking_id = 4 มาจาก PUT /bookings/<id>/status ของฝั่งร้าน)
# ============================================================
def mark_cancelled_by_store(booking_id: int, reason: str = None):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE bookings
        SET cancelled_by = 'store',
            cancellation_reason = %s,
            cancelled_at = NOW()
        WHERE booking_id = %s
    """, (reason, booking_id))

    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated


# ============================================================
#   MINIMUM DAYS REQUIRED BEFORE booking_date TO ALLOW CUSTOMER CANCEL
#   (ตัวอย่าง: จองวันที่ 20 ส.ค. ยกเลิกได้ถึง 18 ส.ค. -- วันที่ 19 ยกเลิกไม่ได้แล้ว)
# ============================================================
CANCEL_MIN_DAYS_BEFORE = 2

# สถานะที่ยังสามารถยกเลิก/ขอเลื่อนนัดได้ (ยังไม่เสร็จสิ้น/ยังไม่ถูกยกเลิก/ไม่มีคำขอเลื่อนนัดค้างอยู่)
_CANCELLABLE_STATUS_IDS = (1, 2)          # pending, confirmed
RESCHEDULABLE_STATUS_IDS = (2,)           # confirmed เท่านั้น (ใช้ร่วมกับ booking_reschedule_service)


def compute_cancel_eligibility(booking_date):
    """คืน (cancellable: bool, days_until: int) คำนวณจากเวลาปัจจุบันฝั่ง Backend
    (Asia/Bangkok) เทียบกับวันนัดจริงเสมอ ห้ามเชื่อค่าจาก Frontend"""
    days_until = (to_date(booking_date) - bangkok_today()).days
    return days_until >= CANCEL_MIN_DAYS_BEFORE, days_until


# ============================================================
#     CANCEL BOOKING BY CUSTOMER (ตรวจสิทธิ์ + สถานะ + กฎ 2 วัน ที่ Backend)
# ============================================================
def cancel_booking_by_customer(booking_id: int, user_id: int, reason: str):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    try:
        conn.begin()

        cur.execute("""
            SELECT booking_id, user_id, store_id, booking_date, booking_time, status_booking_id
            FROM bookings
            WHERE booking_id = %s AND deleted_at IS NULL
            FOR UPDATE
        """, (booking_id,))
        booking = cur.fetchone()

        if not booking:
            conn.rollback()
            raise LookupError("ไม่พบการจองนี้")

        if booking["user_id"] != user_id:
            conn.rollback()
            raise PermissionError("คุณไม่มีสิทธิ์ยกเลิกการจองนี้")

        if booking["status_booking_id"] not in _CANCELLABLE_STATUS_IDS:
            conn.rollback()
            if booking["status_booking_id"] == 3:
                raise ValueError("การจองนี้เสร็จสิ้นแล้ว ไม่สามารถยกเลิกได้")
            if booking["status_booking_id"] == 4:
                raise ValueError("การจองนี้ถูกยกเลิกไปแล้ว")
            raise ValueError("การจองนี้อยู่ระหว่างพิจารณาการเลื่อนนัด ไม่สามารถยกเลิกได้ในขณะนี้")

        cancellable, _days_until = compute_cancel_eligibility(booking["booking_date"])
        if not cancellable:
            conn.rollback()
            raise ValueError(
                "ไม่สามารถยกเลิกการจองได้ เนื่องจากเหลือน้อยกว่า 2 วันก่อนถึงวันนัด "
                "กรุณาติดต่อร้านโดยตรง"
            )

        cur.execute("""
            UPDATE bookings
            SET status_booking_id = 4,
                cancelled_by = 'customer',
                cancellation_reason = %s,
                cancelled_at = NOW(),
                updated_at = NOW()
            WHERE booking_id = %s
        """, (reason, booking_id))

        conn.commit()
        return booking

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#   GET RECENT ALERTS BY STORE
# ============================================================
def get_recent_alerts_by_store(store_id: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT
            booking_id,
            customer_name,
            created_at
        FROM bookings
        WHERE store_id = %s
          AND deleted_at IS NULL
        ORDER BY created_at DESC
        LIMIT 5
    """, (store_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# ============================================================
#   GET schedule BY STORE
# ============================================================
def get_schedule_from_bookings(store_id, date, only_employee_id=None):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        SELECT
            b.booking_id,
            TIME_FORMAT(b.booking_time, '%%H:%%i') AS booking_time,
            b.total_minutes,
            b.customer_name,
            b.employee_id,
            b.status_booking_id,
            IFNULL(e.fullname, 'ยังไม่กำหนด') AS employee_name,
            GROUP_CONCAT(bs.service_id) AS service_ids
        FROM bookings b
        LEFT JOIN employee e ON b.employee_id = e.employee_id
        LEFT JOIN booking_services bs ON b.booking_id = bs.booking_id
        WHERE b.store_id = %s
          AND b.booking_date = %s
          AND b.deleted_at IS NULL
    """
    params = [store_id, date]

    if only_employee_id is not None:
        sql += " AND b.employee_id = %s"
        params.append(only_employee_id)

    sql += " GROUP BY b.booking_id ORDER BY b.booking_time ASC"

    cur.execute(sql, tuple(params))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#   GET schedule DAYS FOR A MONTH (สำหรับจุด indicator บนปฏิทิน)
# ============================================================
def get_schedule_days_for_month(store_id, year, month, only_employee_id=None):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        SELECT b.booking_date AS date, COUNT(*) AS count
        FROM bookings b
        WHERE b.store_id = %s
          AND YEAR(b.booking_date) = %s
          AND MONTH(b.booking_date) = %s
          AND b.deleted_at IS NULL
    """
    params = [store_id, year, month]

    if only_employee_id is not None:
        sql += " AND b.employee_id = %s"
        params.append(only_employee_id)

    sql += " GROUP BY b.booking_date"

    cur.execute(sql, tuple(params))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows



# ============================================================
#     GET SCHEDULE BY DATE (ใช้โดย /schedule/<store_id>/<date>)
# ============================================================
def get_schedule_by_date(store_id, date):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT
            b.booking_id,
            b.booking_time,
            b.customer_name,
            e.fullname AS employee_name
        FROM bookings b
        LEFT JOIN employee e
            ON b.employee_id = e.employee_id
        WHERE b.store_id = %s
          AND DATE(b.booking_date) = %s
          AND b.deleted_at IS NULL
        ORDER BY b.booking_time
    """

    cur.execute(sql, (store_id, date))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


# ============================================================
#     CHECK EMPLOYEE TIME CONFLICT (เดิม - จับคู่เวลาตรงเป๊ะ)
#
#   เก็บไว้เพื่อ backward-compat กับโค้ดอื่นที่อาจยังอ้างอิงอยู่ แต่ตรรกะจองใหม่
#   ทั้งหมด (insert_booking / update_booking / reassign_booking_staff) ใช้
#   booking_eligibility_service.has_time_conflict (ตรวจช่วงเวลาทับซ้อนจริง) แทน
# ============================================================
def check_employee_booking_conflict(employee_id, booking_date, booking_time):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT booking_id
        FROM bookings
        WHERE employee_id = %s
          AND booking_date = %s
          AND booking_time = %s
          AND deleted_at IS NULL
    """, (employee_id, booking_date, booking_time))

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result is not None


# ============================================================
#   GET BOOKED TIMES BY EMPLOYEE
# ============================================================
def get_employee_booked_times(employee_id, booking_date):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT TIME_FORMAT(booking_time,'%%H:%%i') AS booking_time
        FROM bookings
        WHERE employee_id = %s
          AND booking_date = %s
          AND deleted_at IS NULL
    """, (employee_id, booking_date))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows


# ============================================================
#     REASSIGN BOOKING STAFF (เปลี่ยนช่าง + บันทึกประวัติ ในธุรกรรมเดียว)
# ============================================================
def reassign_booking_staff(booking_id: int, new_employee_id: int, reason: str, changed_by=None):
    from services.booking_eligibility_service import (
        get_eligible_employees, has_time_conflict, acquire_employee_date_lock
    )

    conn = get_conn()
    cur = conn.cursor()

    try:
        conn.begin()

        cur.execute("""
            SELECT booking_id, employee_id, store_id, booking_date, booking_time,
                   total_minutes, user_id
            FROM bookings
            WHERE booking_id = %s AND deleted_at IS NULL
            FOR UPDATE
        """, (booking_id,))
        booking = cur.fetchone()
        if not booking:
            conn.rollback()
            raise LookupError("ไม่พบการจองนี้")

        acquire_employee_date_lock(cur, new_employee_id, booking["booking_date"])

        cur.execute("SELECT service_id FROM booking_services WHERE booking_id=%s", (booking_id,))
        service_ids = [r["service_id"] for r in cur.fetchall()]

        eligible = get_eligible_employees(
            booking["store_id"], booking["booking_date"], booking["booking_time"],
            booking["total_minutes"], service_ids, exclude_booking_id=booking_id, cur=cur
        )
        if not any(e["employee_id"] == new_employee_id for e in eligible):
            if has_time_conflict(new_employee_id, booking["booking_date"], booking["booking_time"],
                                  booking["total_minutes"], exclude_booking_id=booking_id, cur=cur):
                raise Exception("พนักงานมีคิวในเวลานี้แล้ว")
            raise Exception("พนักงานไม่สามารถให้บริการในช่วงเวลานี้")

        cur.execute(
            "UPDATE bookings SET employee_id=%s, updated_at=NOW() WHERE booking_id=%s",
            (new_employee_id, booking_id)
        )

        cur.execute("""
            INSERT INTO booking_staff_change_log
                (booking_id, user_id, original_employee_id, new_employee_id, reason, changed_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (booking_id, booking["user_id"], booking["employee_id"], new_employee_id,
              reason, changed_by))

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#     RANDOM-REASSIGN BOOKING STAFF (ช่างเดิมขาดงาน/ลา -> สุ่มใหม่)
#
#   ตรวจ Availability ใหม่ทุกครั้งก่อนสุ่ม (ไม่ใช้รายชื่อเก่าที่อาจไม่ update)
#   คืนค่า dict ของช่างที่ได้ หรือ None ถ้าไม่มีช่างว่างจริง (ห้าม fallback ไป
#   สุ่มจากพนักงานที่ไม่ผ่านเงื่อนไข)
# ============================================================
def random_reassign_booking_staff(booking_id: int, reason: str = "STAFF_ABSENT", changed_by=None):
    from services.booking_eligibility_service import pick_and_lock_employee

    conn = get_conn()
    cur = conn.cursor()

    try:
        conn.begin()

        cur.execute("""
            SELECT booking_id, employee_id, store_id, booking_date, booking_time,
                   total_minutes, user_id
            FROM bookings
            WHERE booking_id = %s AND deleted_at IS NULL
            FOR UPDATE
        """, (booking_id,))
        booking = cur.fetchone()
        if not booking:
            conn.rollback()
            raise LookupError("ไม่พบการจองนี้")

        cur.execute("SELECT service_id FROM booking_services WHERE booking_id=%s", (booking_id,))
        service_ids = [r["service_id"] for r in cur.fetchall()]

        new_employee_id = pick_and_lock_employee(
            cur, booking["store_id"], booking["booking_date"], booking["booking_time"],
            booking["total_minutes"], service_ids, exclude_booking_id=booking_id
        )

        if not new_employee_id:
            conn.rollback()
            return None

        cur.execute(
            "UPDATE bookings SET employee_id=%s, updated_at=NOW() WHERE booking_id=%s",
            (new_employee_id, booking_id)
        )

        cur.execute("""
            INSERT INTO booking_staff_change_log
                (booking_id, user_id, original_employee_id, new_employee_id, reason, changed_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (booking_id, booking["user_id"], booking["employee_id"], new_employee_id,
              reason, changed_by))

        conn.commit()
        return {"employee_id": new_employee_id}

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#     GET BOOKING STAFF-CHANGE HISTORY
# ============================================================
def get_booking_staff_history(booking_id: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT
            bscl.change_id,
            bscl.booking_id,
            bscl.original_employee_id,
            oe.fullname AS original_employee_name,
            bscl.new_employee_id,
            ne.fullname AS new_employee_name,
            bscl.reason,
            bscl.note,
            bscl.changed_by,
            bscl.changed_at
        FROM booking_staff_change_log bscl
        LEFT JOIN employee oe ON bscl.original_employee_id = oe.employee_id
        LEFT JOIN employee ne ON bscl.new_employee_id = ne.employee_id
        WHERE bscl.booking_id = %s
        ORDER BY bscl.changed_at DESC
    """, (booking_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#   ตัดคิวที่เวลาผ่านไปแล้วออก (เทียบกับเวลาปัจจุบันแบบ Asia/Bangkok)
#   ใช้ร่วมกันระหว่าง get_affected_bookings_for_employee/for_store
# ============================================================
def _filter_not_passed(rows: list, target_date):
    is_today = target_date == bangkok_today()
    now_time = bangkok_time_now() if is_today else None

    result = []
    for row in rows:
        raw_time = row.pop("raw_booking_time")
        if is_today and raw_time is not None:
            # pymysql คืนค่า TIME เป็น timedelta -> แปลงเป็น time เพื่อเทียบ
            total_seconds = int(raw_time.total_seconds())
            row_time = (total_seconds // 3600, (total_seconds % 3600) // 60, total_seconds % 60)
            now_tuple = (now_time.hour, now_time.minute, now_time.second)
            if row_time <= now_tuple:
                continue
        result.append(row)

    return result


# ============================================================
#     GET AFFECTED BOOKINGS FOR AN ABSENT/LEAVE EMPLOYEE
#
#   เงื่อนไข: เป็นของช่างคนนั้น, วันที่ตรงกับวันที่ระบุ, สถานะยังไม่เสร็จ/ยังไม่
#   ยกเลิก, เวลาให้บริการยังไม่ผ่าน (เทียบกับเวลาปัจจุบันแบบ Asia/Bangkok)
#   ไม่ลบ Appointment เดิมใด ๆ ทั้งสิ้น
# ============================================================
def get_affected_bookings_for_employee(employee_id: int, absence_date):
    absence_date = to_date(absence_date)

    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT
            b.booking_id,
            b.customer_name,
            b.customer_phone,
            b.booking_date,
            TIME_FORMAT(b.booking_time, '%%H:%%i') AS booking_time,
            b.booking_time AS raw_booking_time,
            b.employee_id,
            b.status_booking_id,
            sb.status_booking_name,
            b.assignment_type,
            b.total_minutes,
            GROUP_CONCAT(bs.service_name SEPARATOR ', ') AS services,
            GROUP_CONCAT(bs.service_id) AS service_ids
        FROM bookings b
        LEFT JOIN status_booking sb ON b.status_booking_id = sb.status_booking_id
        LEFT JOIN booking_services bs ON b.booking_id = bs.booking_id
        WHERE b.employee_id = %s
          AND b.booking_date = %s
          AND b.deleted_at IS NULL
          AND b.status_booking_id NOT IN (3, 4)
        GROUP BY b.booking_id
        ORDER BY b.booking_time
    """, (employee_id, absence_date))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return _filter_not_passed(rows, absence_date)


# ============================================================
#   GET AFFECTED BOOKINGS FOR THE WHOLE STORE (สำหรับ Dashboard)
#
#   คิวทั้งหมดของวันที่ระบุ ที่ช่างที่ถูกมอบหมาย "ขาดงาน" (ACTIVE ABSENT) อยู่
# ============================================================
def get_affected_bookings_for_store(store_id: int, target_date):
    target_date = to_date(target_date)

    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT
            b.booking_id,
            b.customer_name,
            b.customer_phone,
            b.booking_date,
            TIME_FORMAT(b.booking_time, '%%H:%%i') AS booking_time,
            b.booking_time AS raw_booking_time,
            b.employee_id,
            e.fullname AS employee_name,
            b.status_booking_id,
            sb.status_booking_name,
            b.total_minutes,
            GROUP_CONCAT(bs.service_name SEPARATOR ', ') AS services,
            GROUP_CONCAT(bs.service_id) AS service_ids
        FROM bookings b
        JOIN employee_absence ea
            ON ea.employee_id = b.employee_id
           AND ea.absence_date = b.booking_date
           AND ea.absence_type = 'ABSENT'
           AND ea.status = 'ACTIVE'
        LEFT JOIN employee e ON b.employee_id = e.employee_id
        LEFT JOIN status_booking sb ON b.status_booking_id = sb.status_booking_id
        LEFT JOIN booking_services bs ON b.booking_id = bs.booking_id
        WHERE b.store_id = %s
          AND b.booking_date = %s
          AND b.deleted_at IS NULL
          AND b.status_booking_id NOT IN (3, 4)
        GROUP BY b.booking_id
        ORDER BY b.booking_time
    """, (store_id, target_date))

    rows = cur.fetchall()
    cur.close()
    conn.close()

    return _filter_not_passed(rows, target_date)


# ============================================================
#     เปลี่ยนบริการของคิว (สำหรับกรณี "ไม่มีช่างว่าง" -> ลองเปลี่ยนบริการ)
#
#   แทนที่รายการ booking_services ทั้งหมดของคิวนี้ + คำนวณ total_price/
#   total_minutes ใหม่ ในธุรกรรมเดียว ถ้าช่างเดิมที่ผูกไว้ไม่มีทักษะตรงกับ
#   บริการชุดใหม่ จะถอดช่างออก (employee_id = NULL) แทนที่จะปล่อยให้ค้างผิด
#   เงื่อนไข -- ไม่ auto เปลี่ยนช่างให้เอง ต้องให้ admin ไปกดเปลี่ยนช่างต่อเอง
# ============================================================
def replace_booking_services(booking_id: int, services: list):
    from services.booking_eligibility_service import get_eligible_employees

    if not services:
        raise ValueError("ต้องเลือกบริการอย่างน้อย 1 รายการ")

    total_price = sum(float(s["price"]) for s in services)
    total_minutes = sum(int(s["minutes"]) for s in services)
    service_ids = [s["service_id"] for s in services]

    conn = get_conn()
    cur = conn.cursor()

    try:
        conn.begin()

        cur.execute("""
            SELECT booking_id, employee_id, store_id, booking_date, booking_time
            FROM bookings WHERE booking_id = %s AND deleted_at IS NULL
            FOR UPDATE
        """, (booking_id,))
        booking = cur.fetchone()
        if not booking:
            conn.rollback()
            raise LookupError("ไม่พบการจองนี้")

        cur.execute("DELETE FROM booking_services WHERE booking_id = %s", (booking_id,))
        cur.executemany("""
            INSERT INTO booking_services
                (booking_id, service_id, service_name, service_price, service_minutes)
            VALUES (%s, %s, %s, %s, %s)
        """, [
            (booking_id, s["service_id"], s["name"], s["price"], s["minutes"])
            for s in services
        ])

        new_employee_id = booking["employee_id"]
        if new_employee_id:
            eligible = get_eligible_employees(
                booking["store_id"], booking["booking_date"], booking["booking_time"],
                total_minutes, service_ids, exclude_booking_id=booking_id, cur=cur
            )
            if not any(e["employee_id"] == new_employee_id for e in eligible):
                new_employee_id = None

        cur.execute("""
            UPDATE bookings
            SET total_price = %s, total_minutes = %s, employee_id = %s, updated_at = NOW()
            WHERE booking_id = %s
        """, (total_price, total_minutes, new_employee_id, booking_id))

        conn.commit()
        return {"employee_unassigned": new_employee_id != booking["employee_id"]}

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()
