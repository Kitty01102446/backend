"""
ระบบขอเลื่อนนัด (Reschedule Request) -- ทั้งฝั่งลูกค้าขอเลื่อน และฝั่งร้านขอเลื่อน

ไม่เปลี่ยนวัน/เวลาของ booking ทันทีตอนขอ -- แค่สร้างคำขอ (booking_reschedule_request,
status='pending') แล้วเปลี่ยน bookings.status_booking_id เป็นสถานะ "รอพิจารณา" เท่านั้น
ต้องรอให้อีกฝ่ายอนุมัติ (approve/accept) ก่อน จึงจะย้ายวัน/เวลาจริงและตรวจสอบ
Eligibility + คิวชนใหม่ทั้งหมด (reuse booking_eligibility_service เหมือนกับ update_booking)
"""

from datetime import datetime, time as time_cls

import pymysql

from services.db import get_conn
from services.timeutil import bangkok_now, combine_bkk, to_date
from services.booking_service import RESCHEDULABLE_STATUS_IDS, compute_cancel_eligibility

# ข้อความเดียวกับตอนยกเลิก -- ลูกค้าขอเลื่อนนัดได้ก็ต่อเมื่อยังยกเลิกได้ (เหลืออย่างน้อย 2
# วันก่อนถึงวันนัดเดิม) เงื่อนไขเดียวกันนี้กันการจองที่ผ่านมาแล้วโดยอัตโนมัติด้วย เพราะ
# compute_cancel_eligibility คำนวณจากวันที่ปัจจุบันฝั่ง Backend เทียบกับวันนัดจริงเสมอ
_RESCHEDULE_TOO_LATE_MESSAGE = (
    "ไม่สามารถขอเลื่อนนัดได้ เนื่องจากเหลือน้อยกว่า 2 วันก่อนถึงวันนัด หรือวันนัดผ่านไปแล้ว "
    "กรุณาติดต่อร้านโดยตรง"
)


def _to_time_obj(value) -> time_cls:
    if isinstance(value, time_cls):
        return value
    text = str(value)
    if len(text) == 5:  # "HH:MM"
        text += ":00"
    return datetime.strptime(text, "%H:%M:%S").time()


def _status_blocked_message(status_booking_id: int) -> str:
    if status_booking_id in (5, 6):
        return "มีคำขอเลื่อนนัดที่รอดำเนินการอยู่แล้ว"
    if status_booking_id == 1:
        return "การจองนี้ยังไม่ได้รับการยืนยันจากร้าน ไม่สามารถขอเลื่อนนัดได้"
    if status_booking_id == 3:
        return "การจองนี้เสร็จสิ้นแล้ว ไม่สามารถขอเลื่อนนัดได้"
    if status_booking_id == 4:
        return "การจองนี้ถูกยกเลิกไปแล้ว"
    return "การจองนี้ไม่สามารถขอเลื่อนนัดได้ในขณะนี้"


def _load_request_for_update(cur, request_id):
    cur.execute(
        "SELECT * FROM booking_reschedule_request WHERE request_id = %s FOR UPDATE",
        (request_id,)
    )
    req = cur.fetchone()
    if not req:
        raise LookupError("ไม่พบคำขอเลื่อนนัดนี้")
    return req


def _load_booking_for_update(cur, booking_id):
    cur.execute("""
        SELECT booking_id, user_id, store_id, employee_id, booking_date, booking_time,
               total_minutes, status_booking_id
        FROM bookings
        WHERE booking_id = %s AND deleted_at IS NULL
        FOR UPDATE
    """, (booking_id,))
    booking = cur.fetchone()
    if not booking:
        raise LookupError("ไม่พบการจองนี้")
    return booking


def _apply_approved_reschedule(cur, request, booking):
    """ย้ายวัน/เวลาจริง -- ตรวจ Eligibility + คิวชนใหม่ทั้งหมดก่อนเสมอ (เหมือน update_booking)"""
    from services.booking_eligibility_service import (
        get_eligible_employees, has_time_conflict, acquire_employee_date_lock,
    )

    cur.execute("SELECT service_id FROM booking_services WHERE booking_id=%s", (booking["booking_id"],))
    service_ids = [r["service_id"] for r in cur.fetchall()]

    if booking["employee_id"]:
        acquire_employee_date_lock(cur, booking["employee_id"], request["proposed_date"])

        eligible = get_eligible_employees(
            booking["store_id"], request["proposed_date"], request["proposed_time"],
            booking["total_minutes"], service_ids,
            exclude_booking_id=booking["booking_id"], cur=cur
        )
        if not any(e["employee_id"] == booking["employee_id"] for e in eligible):
            if has_time_conflict(booking["employee_id"], request["proposed_date"], request["proposed_time"],
                                  booking["total_minutes"], exclude_booking_id=booking["booking_id"], cur=cur):
                raise Exception("พนักงานมีคิวในเวลานี้แล้ว")
            raise Exception("พนักงานไม่สามารถให้บริการในช่วงเวลานี้")

    cur.execute("""
        UPDATE bookings
        SET booking_date = %s, booking_time = %s, status_booking_id = 2, updated_at = NOW()
        WHERE booking_id = %s
    """, (request["proposed_date"], request["proposed_time"], booking["booking_id"]))

    cur.execute("""
        UPDATE booking_reschedule_request
        SET status = 'approved', responded_at = NOW()
        WHERE request_id = %s
    """, (request["request_id"],))


def _reject_and_restore(cur, request, booking, response_note):
    cur.execute("""
        UPDATE bookings SET status_booking_id = 2, updated_at = NOW() WHERE booking_id = %s
    """, (booking["booking_id"],))

    cur.execute("""
        UPDATE booking_reschedule_request
        SET status = 'rejected', response_note = %s, responded_at = NOW()
        WHERE request_id = %s
    """, (response_note, request["request_id"]))


# ============================================================
#   CREATE RESCHEDULE REQUEST (ฝั่งลูกค้าหรือฝั่งร้าน)
# ============================================================
def create_reschedule_request(booking_id: int, requested_by: str, actor_user_id: int,
                               proposed_date, proposed_time, reason: str):
    if requested_by not in ("customer", "store"):
        raise ValueError("requested_by ไม่ถูกต้อง")

    proposed_date_obj = to_date(proposed_date)
    proposed_time_obj = _to_time_obj(proposed_time)

    if combine_bkk(proposed_date_obj, proposed_time_obj) <= bangkok_now():
        raise ValueError("ไม่สามารถขอเลื่อนเป็นวัน/เวลาในอดีตได้")

    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    try:
        conn.begin()

        booking = _load_booking_for_update(cur, booking_id)

        if requested_by == "customer" and booking["user_id"] != actor_user_id:
            conn.rollback()
            raise PermissionError("คุณไม่มีสิทธิ์ขอเลื่อนนัดการจองนี้")

        if booking["status_booking_id"] not in RESCHEDULABLE_STATUS_IDS:
            conn.rollback()
            raise ValueError(_status_blocked_message(booking["status_booking_id"]))

        if requested_by == "customer":
            cancellable, _days_until = compute_cancel_eligibility(booking["booking_date"])
            if not cancellable:
                conn.rollback()
                raise ValueError(_RESCHEDULE_TOO_LATE_MESSAGE)

        cur.execute("""
            INSERT INTO booking_reschedule_request
                (booking_id, requested_by, old_date, old_time, proposed_date, proposed_time,
                 reason, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, 'pending', NOW())
        """, (
            booking_id, requested_by, booking["booking_date"], booking["booking_time"],
            proposed_date_obj, proposed_time_obj, reason,
        ))
        request_id = cur.lastrowid

        new_status = 5 if requested_by == "customer" else 6
        cur.execute(
            "UPDATE bookings SET status_booking_id = %s, updated_at = NOW() WHERE booking_id = %s",
            (new_status, booking_id)
        )

        conn.commit()
        return {"request_id": request_id, "booking": booking}

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#   APPROVE RESCHEDULE REQUEST (ฝั่งร้าน อนุมัติคำขอที่ลูกค้าส่งมา)
# ============================================================
def approve_reschedule_request(request_id: int, responder_user_id: int = None):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    try:
        conn.begin()

        request = _load_request_for_update(cur, request_id)
        if request["status"] != "pending":
            conn.rollback()
            raise ValueError("คำขอนี้ถูกดำเนินการไปแล้ว")
        if request["requested_by"] != "customer":
            conn.rollback()
            raise ValueError("คำขอนี้ไม่ใช่คำขอจากลูกค้า")

        booking = _load_booking_for_update(cur, request["booking_id"])
        _apply_approved_reschedule(cur, request, booking)

        conn.commit()
        return {"request": request, "booking": booking}

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#   REJECT RESCHEDULE REQUEST (ฝั่งร้าน ปฏิเสธคำขอที่ลูกค้าส่งมา)
# ============================================================
def reject_reschedule_request(request_id: int, responder_user_id: int = None, response_note: str = None):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    try:
        conn.begin()

        request = _load_request_for_update(cur, request_id)
        if request["status"] != "pending":
            conn.rollback()
            raise ValueError("คำขอนี้ถูกดำเนินการไปแล้ว")
        if request["requested_by"] != "customer":
            conn.rollback()
            raise ValueError("คำขอนี้ไม่ใช่คำขอจากลูกค้า")

        booking = _load_booking_for_update(cur, request["booking_id"])
        _reject_and_restore(cur, request, booking, response_note)

        conn.commit()
        return {"request": request, "booking": booking}

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#   CUSTOMER RESPONDS TO A STORE-INITIATED RESCHEDULE REQUEST
# ============================================================
def respond_to_store_reschedule(request_id: int, customer_user_id: int, accept: bool, response_note: str = None):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    try:
        conn.begin()

        request = _load_request_for_update(cur, request_id)
        if request["status"] != "pending":
            conn.rollback()
            raise ValueError("คำขอนี้ถูกดำเนินการไปแล้ว")
        if request["requested_by"] != "store":
            conn.rollback()
            raise ValueError("คำขอนี้ไม่ใช่คำขอจากร้าน")

        booking = _load_booking_for_update(cur, request["booking_id"])
        if booking["user_id"] != customer_user_id:
            conn.rollback()
            raise PermissionError("คุณไม่มีสิทธิ์ตอบคำขอนี้")

        if accept:
            _apply_approved_reschedule(cur, request, booking)
        else:
            _reject_and_restore(cur, request, booking, response_note)

        conn.commit()
        return {"request": request, "booking": booking}

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()


# ============================================================
#   READ HELPERS
# ============================================================
def get_reschedule_request_by_id(request_id: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute("SELECT * FROM booking_reschedule_request WHERE request_id = %s", (request_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


_JSON_SAFE_SELECT = """
    SELECT
        request_id, booking_id, requested_by,
        DATE_FORMAT(old_date, '%%Y-%%m-%%d') AS old_date,
        TIME_FORMAT(old_time, '%%H:%%i') AS old_time,
        DATE_FORMAT(proposed_date, '%%Y-%%m-%%d') AS proposed_date,
        TIME_FORMAT(proposed_time, '%%H:%%i') AS proposed_time,
        reason, status, response_note, created_at, responded_at
    FROM booking_reschedule_request
"""


def get_pending_request_for_booking(booking_id: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f"""
        {_JSON_SAFE_SELECT}
        WHERE booking_id = %s AND status = 'pending'
        ORDER BY created_at DESC
        LIMIT 1
    """, (booking_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def get_latest_request_for_booking(booking_id: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(f"""
        {_JSON_SAFE_SELECT}
        WHERE booking_id = %s
        ORDER BY created_at DESC
        LIMIT 1
    """, (booking_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row
