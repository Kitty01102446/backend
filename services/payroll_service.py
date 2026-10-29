"""
ระบบเงินเดือน (เฟส 2)

โครงสร้างค่าจ้าง = เงินเดือนฐาน (base_salary) + คอมมิชชั่นจากยอดบริการที่ทำ
สำเร็จ (commission_rate %) ตามที่ผู้ใช้เลือกไว้ ไม่มีการคำนวณ OT เพราะระบบยัง
ไม่มีข้อมูลชั่วโมงทำงานจริง (clock-in/out)

สำคัญ: กรณี Absent จะถูก "บันทึกไว้" เป็นข้อมูล (absent_days) เท่านั้น
ไม่ได้ถูกหักออกจาก base_salary โดยอัตโนมัติ -- Admin ต้องตรวจสอบและกดยืนยัน
(confirm_payroll) ก่อน โดยสามารถแก้ไข total_amount เองได้ก่อนยืนยันเสมอ
"""

import calendar
from services.db import get_conn
from services.timeutil import bangkok_now


# ============================================================
#   ตั้ง/แก้อัตราค่าจ้างของพนักงาน
# ============================================================
def set_employee_pay_rate(employee_id: int, base_salary, commission_rate):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE employee
        SET base_salary = %s, commission_rate = %s
        WHERE employee_id = %s AND deleted_at IS NULL
    """, (base_salary, commission_rate, employee_id))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#   คำนวณ "ร่าง" เงินเดือนของพนักงาน 1 คน สำหรับเดือน/ปีที่ระบุ
#
#   ถ้ามี payroll_record อยู่แล้วและสถานะเป็น CONFIRMED จะไม่คำนวณทับ (คืนค่า
#   record เดิมตรง ๆ) ถ้ายังเป็น DRAFT หรือยังไม่มี record จะคำนวณใหม่เสมอ
# ============================================================
def compute_draft_payroll(employee_id: int, year: int, month: int):
    conn = get_conn()
    cur = conn.cursor()

    try:
        conn.begin()

        cur.execute("""
            SELECT * FROM payroll_record
            WHERE employee_id = %s AND period_year = %s AND period_month = %s
            FOR UPDATE
        """, (employee_id, year, month))
        existing = cur.fetchone()

        if existing and existing["status"] == "CONFIRMED":
            conn.rollback()
            return existing

        cur.execute("""
            SELECT employee_id, store_id, base_salary, commission_rate
            FROM employee WHERE employee_id = %s AND deleted_at IS NULL
        """, (employee_id,))
        emp = cur.fetchone()
        if not emp:
            conn.rollback()
            raise LookupError("ไม่พบพนักงานนี้")

        total_days = calendar.monthrange(year, month)[1]

        cur.execute("""
            SELECT COALESCE(SUM(CASE WHEN leave_scope = 'HALF_DAY' THEN 0.5 ELSE 1 END), 0) AS leave_days
            FROM employee_absence
            WHERE employee_id = %s AND absence_type = 'LEAVE' AND status = 'ACTIVE'
              AND YEAR(absence_date) = %s AND MONTH(absence_date) = %s
        """, (employee_id, year, month))
        leave_days = float(cur.fetchone()["leave_days"])

        cur.execute("""
            SELECT COUNT(*) AS absent_days
            FROM employee_absence
            WHERE employee_id = %s AND absence_type = 'ABSENT' AND status = 'ACTIVE'
              AND YEAR(absence_date) = %s AND MONTH(absence_date) = %s
        """, (employee_id, year, month))
        absent_days = int(cur.fetchone()["absent_days"])

        work_days = max(total_days - leave_days - absent_days, 0)

        commission_rate = float(emp["commission_rate"] or 0)
        cur.execute("""
            SELECT COALESCE(SUM(total_price), 0) AS revenue
            FROM bookings
            WHERE employee_id = %s AND status_booking_id = 3 AND deleted_at IS NULL
              AND YEAR(booking_date) = %s AND MONTH(booking_date) = %s
        """, (employee_id, year, month))
        revenue = float(cur.fetchone()["revenue"])
        commission_amount = round(revenue * commission_rate / 100, 2)

        base_salary = float(emp["base_salary"] or 0)
        total_amount = round(base_salary + commission_amount, 2)

        if existing:
            cur.execute("""
                UPDATE payroll_record
                SET work_days=%s, leave_days=%s, absent_days=%s,
                    base_salary=%s, commission_amount=%s, total_amount=%s,
                    updated_at=NOW()
                WHERE payroll_id = %s
            """, (work_days, leave_days, absent_days, base_salary,
                  commission_amount, total_amount, existing["payroll_id"]))
            payroll_id = existing["payroll_id"]
        else:
            cur.execute("""
                INSERT INTO payroll_record
                    (employee_id, store_id, period_year, period_month,
                     work_days, leave_days, absent_days,
                     base_salary, commission_amount, total_amount, status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'DRAFT')
            """, (employee_id, emp["store_id"], year, month,
                  work_days, leave_days, absent_days,
                  base_salary, commission_amount, total_amount))
            payroll_id = cur.lastrowid

        conn.commit()

        cur.execute("SELECT * FROM payroll_record WHERE payroll_id = %s", (payroll_id,))
        result = cur.fetchone()
        return result

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#   สรุปเงินเดือนของพนักงานทุกคนในร้าน สำหรับเดือน/ปีที่ระบุ (คำนวณร่างให้ทุกคน)
# ============================================================
def get_store_payroll(store_id: int, year: int, month: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT employee_id FROM employee
        WHERE store_id = %s AND deleted_at IS NULL
        ORDER BY employee_id
    """, (store_id,))
    employee_ids = [r["employee_id"] for r in cur.fetchall()]

    cur.close()
    conn.close()

    return [compute_draft_payroll(eid, year, month) for eid in employee_ids]


# ============================================================
#   ยืนยันเงินเดือน (Admin ตรวจสอบแล้ว, แก้ยอดได้ก่อนยืนยัน)
# ============================================================
def confirm_payroll(employee_id: int, year: int, month: int, confirmed_by=None, total_amount_override=None):
    record = compute_draft_payroll(employee_id, year, month)

    conn = get_conn()
    cur = conn.cursor()

    final_total = total_amount_override if total_amount_override is not None else record["total_amount"]

    cur.execute("""
        UPDATE payroll_record
        SET status = 'CONFIRMED', total_amount = %s,
            confirmed_by = %s, confirmed_at = %s, updated_at = NOW()
        WHERE payroll_id = %s
    """, (final_total, confirmed_by, bangkok_now(), record["payroll_id"]))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#   ประวัติเงินเดือนของพนักงาน 1 คน
# ============================================================
def get_employee_payroll_history(employee_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM payroll_record
        WHERE employee_id = %s
        ORDER BY period_year DESC, period_month DESC
    """, (employee_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
