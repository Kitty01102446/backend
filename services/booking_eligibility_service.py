"""
เอนจินตรวจสอบความพร้อมของพนักงาน (Eligible Staff) และการสุ่มช่าง

รวมเงื่อนไขทั้งหมดที่ต้องผ่านก่อนพนักงานจะ "รับงานได้/ถูกสุ่มเลือกได้":
  1. มีทักษะตรงกับบริการที่เลือกครบทุกรายการ (employee_service_skill)
  2. ไม่ติดวันลา/ขาดงาน/วันหยุดที่ครอบคลุมวัน-เวลานั้น (employee_absence)
  3. อยู่ในช่วงเวลาทำงาน ถ้ามีการตั้งค่าไว้ (employee_work_hours) —
     ถ้ายังไม่มีการตั้งค่าเลย ถือว่าทำงานได้ไม่จำกัดเวลา (ย้อนหลังเข้ากันได้)
  4. ไม่มีคิวชนกัน (ตรวจแบบช่วงเวลาทับซ้อนจริง ไม่ใช่ตรงเป๊ะ)
  5. ถ้าวันที่จองคือวันนี้ สถานะปัจจุบัน (current_status_id) ต้องไม่ใช่ leave/absent/off

ห้าม random จากพนักงานทั้งหมดโดยไม่กรองก่อนเด็ดขาด
"""

import random
from services.db import get_conn
from services.timeutil import bangkok_today, iso_day_of_week, to_date


# ============================================================
#   CHECK TIME CONFLICT (ช่วงเวลาทับซ้อนจริง ไม่ใช่ตรงเป๊ะ)
# ============================================================
def has_time_conflict(employee_id, booking_date, booking_time, total_minutes,
                       exclude_booking_id=None, cur=None):
    own_conn = None
    if cur is None:
        own_conn = get_conn()
        cur = own_conn.cursor()

    try:
        cur.execute("""
            SELECT booking_id
            FROM bookings
            WHERE employee_id = %(employee_id)s
              AND booking_date = %(booking_date)s
              AND deleted_at IS NULL
              AND status_booking_id != 4
              AND (%(exclude_id)s IS NULL OR booking_id != %(exclude_id)s)
              AND booking_time < ADDTIME(%(start)s, SEC_TO_TIME(%(minutes)s * 60))
              AND ADDTIME(booking_time, SEC_TO_TIME(COALESCE(total_minutes, 0) * 60)) > %(start)s
            LIMIT 1
        """, {
            "employee_id": employee_id,
            "booking_date": booking_date,
            "exclude_id": exclude_booking_id,
            "start": booking_time,
            "minutes": total_minutes or 0,
        })
        return cur.fetchone() is not None
    finally:
        if own_conn is not None:
            cur.close()
            own_conn.close()


# ============================================================
#   GET ELIGIBLE EMPLOYEES (พนักงานที่พร้อมรับงานจริง)
# ============================================================
def get_eligible_employees(store_id, booking_date, booking_time, total_minutes,
                            service_ids, exclude_booking_id=None, cur=None):
    service_ids = [sid for sid in (service_ids or []) if sid is not None]
    if not service_ids:
        return []

    booking_date = to_date(booking_date)

    own_conn = None
    if cur is None:
        own_conn = get_conn()
        cur = own_conn.cursor()

    try:
        service_keys = []
        params = {
            "store_id": store_id,
            "service_count": len(service_ids),
            "booking_date": booking_date,
            "start": booking_time,
            "minutes": total_minutes or 0,
            "iso_dow": iso_day_of_week(booking_date),
            "exclude_id": exclude_booking_id,
            "is_today": 1 if booking_date == bangkok_today() else 0,
        }
        for idx, sid in enumerate(service_ids):
            key = f"svc{idx}"
            service_keys.append(f"%({key})s")
            params[key] = sid
        service_in_clause = ", ".join(service_keys)

        sql = f"""
            SELECT e.employee_id, e.fullname
            FROM employee e
            WHERE e.store_id = %(store_id)s
              AND e.deleted_at IS NULL
              AND (
                SELECT COUNT(DISTINCT ess.service_id)
                FROM employee_service_skill ess
                WHERE ess.employee_id = e.employee_id
                  AND ess.service_id IN ({service_in_clause})
              ) = %(service_count)s
              AND NOT EXISTS (
                SELECT 1 FROM employee_absence ea
                WHERE ea.employee_id = e.employee_id
                  AND ea.absence_date = %(booking_date)s
                  AND ea.status = 'ACTIVE'
                  AND (
                    ea.leave_scope IS NULL
                    OR ea.leave_scope = 'FULL_DAY'
                    OR (ea.start_time < ADDTIME(%(start)s, SEC_TO_TIME(%(minutes)s * 60))
                        AND ea.end_time > %(start)s)
                  )
              )
              AND (
                NOT EXISTS (SELECT 1 FROM employee_work_hours ewh WHERE ewh.employee_id = e.employee_id)
                OR EXISTS (
                  SELECT 1 FROM employee_work_hours ewh
                  WHERE ewh.employee_id = e.employee_id
                    AND ewh.day_of_week = %(iso_dow)s
                    AND ewh.is_working = 1
                    AND ewh.start_time <= %(start)s
                    AND ewh.end_time >= ADDTIME(%(start)s, SEC_TO_TIME(%(minutes)s * 60))
                )
              )
              AND NOT EXISTS (
                SELECT 1 FROM bookings b
                WHERE b.employee_id = e.employee_id
                  AND b.booking_date = %(booking_date)s
                  AND b.deleted_at IS NULL
                  AND b.status_booking_id != 4
                  AND (%(exclude_id)s IS NULL OR b.booking_id != %(exclude_id)s)
                  AND b.booking_time < ADDTIME(%(start)s, SEC_TO_TIME(%(minutes)s * 60))
                  AND ADDTIME(b.booking_time, SEC_TO_TIME(COALESCE(b.total_minutes, 0) * 60)) > %(start)s
              )
              AND (
                %(is_today)s = 0
                OR e.current_status_id IS NULL
                OR e.current_status_id NOT IN (
                  SELECT status_employee_id FROM status_employee
                  WHERE status_employee_name IN ('leave', 'absent', 'off')
                )
              )
            ORDER BY e.employee_id
        """

        cur.execute(sql, params)
        return cur.fetchall()
    finally:
        if own_conn is not None:
            cur.close()
            own_conn.close()


# ============================================================
#   RANDOM PICK (สุ่มจาก Eligible Staff เท่านั้น ตรวจใหม่ทุกครั้ง)
# ============================================================
def random_pick_employee(store_id, booking_date, booking_time, total_minutes,
                          service_ids, exclude_booking_id=None, cur=None):
    candidates = get_eligible_employees(
        store_id, booking_date, booking_time, total_minutes,
        service_ids, exclude_booking_id=exclude_booking_id, cur=cur
    )
    if not candidates:
        return None
    return random.choice(candidates)


# ============================================================
#   ACQUIRE EMPLOYEE-DATE LOCK (ต้องเรียกภายใน conn.begin() แล้วเท่านั้น)
# ============================================================
def acquire_employee_date_lock(cur, employee_id, booking_date):
    cur.execute(
        "INSERT INTO employee_date_lock (employee_id, lock_date) VALUES (%s, %s) "
        "ON DUPLICATE KEY UPDATE employee_id = employee_id",
        (employee_id, booking_date)
    )
    cur.execute(
        "SELECT employee_id FROM employee_date_lock WHERE employee_id=%s AND lock_date=%s FOR UPDATE",
        (employee_id, booking_date)
    )


# ============================================================
#   PICK + LOCK AN ELIGIBLE EMPLOYEE (สำหรับ System Match / Random Reassign)
#
#   ต้องเรียกภายใน conn.begin() ที่เปิดไว้แล้วเท่านั้น (ใช้ cursor เดียวกัน)
#   สุ่มลำดับผู้สมัครแล้วล็อกทีละคน ตรวจสอบ eligibility ซ้ำหลังล็อกทุกครั้ง
#   (กันกรณี request อื่นแย่งคิวไปในช่วงเวลาสั้น ๆ ระหว่างคำนวณรายชื่อผู้สมัคร)
#   คืนค่า employee_id ที่ล็อกสำเร็จ หรือ None ถ้าไม่มีใครว่างจริง
# ============================================================
def pick_and_lock_employee(cur, store_id, booking_date, booking_time, total_minutes,
                            service_ids, exclude_booking_id=None):
    candidates = get_eligible_employees(
        store_id, booking_date, booking_time, total_minutes,
        service_ids, exclude_booking_id=exclude_booking_id, cur=cur
    )
    candidate_ids = [c["employee_id"] for c in candidates]
    random.shuffle(candidate_ids)

    for candidate_id in candidate_ids:
        acquire_employee_date_lock(cur, candidate_id, booking_date)

        still_eligible = get_eligible_employees(
            store_id, booking_date, booking_time, total_minutes,
            service_ids, exclude_booking_id=exclude_booking_id, cur=cur
        )
        if any(e["employee_id"] == candidate_id for e in still_eligible):
            return candidate_id

    return None
