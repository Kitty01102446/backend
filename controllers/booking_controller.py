import os
import sys
from services.booking_service import get_store_bookings
from services.booking_service import (
    get_all_booking,
    get_booking_by_id,
    insert_booking,
    update_booking,
    delete_booking,
    get_booking_with_services,
    insert_booking_services,
    get_user_bookings,
    get_store_bookings,
    update_booking_status_service,
    get_recent_alerts_by_store,
    get_schedule_from_bookings,
    get_employee_booked_times,
    reassign_booking_staff,
    random_reassign_booking_staff,
    get_booking_staff_history,
    get_affected_bookings_for_employee,
    get_affected_bookings_for_store,
    replace_booking_services,
    get_schedule_days_for_month,
)
from services.booking_service import (
    cancel_booking_by_customer,
    compute_cancel_eligibility,
    mark_cancelled_by_store,
)
from services.booking_reschedule_service import (
    create_reschedule_request,
    approve_reschedule_request,
    reject_reschedule_request,
    respond_to_store_reschedule,
    get_reschedule_request_by_id,
    get_latest_request_for_booking,
)
from services.notification_service import create_notification
from services.store_service import get_store_owner_user_id
from services.timeutil import bangkok_today
from flask import current_app, g
from services.auth_service import (
    token_required,
    require_store_owner,
    require_booking_store_owner,
    require_booking_customer_owner,
    require_self_user,
    require_employee_access,
)
import datetime as _dt




# ✅ บังคับให้ Python มองเห็นโฟลเดอร์หลัก (backend)
# เพื่อให้ import services หรือ config ได้ถูกต้อง
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Blueprint, request, jsonify
# ตอนนี้ Python จะหาโฟลเดอร์ services เจอแล้ว
from services.booking_service import (
    get_all_booking,
    get_booking_by_id,
    insert_booking,
    update_booking,
    delete_booking,
    get_booking_with_services,
    insert_booking_services,
    get_user_bookings
)

booking_bp = Blueprint("booking_bp", __name__)

# ข้อความ error ที่หมายถึง "ช่างไม่พร้อมให้บริการ" (ทักษะ/ลา/ขาดงาน/เวลาทำงาน/คิวชน)
# ใช้แยกว่าควรตอบ 409 (ขัดแย้งกับสถานะปัจจุบัน) แทน 400 (ข้อมูลไม่ถูกต้อง)
_ELIGIBILITY_ERROR_MESSAGES = (
    "พนักงานมีคิวในเวลานี้แล้ว",
    "พนักงานไม่สามารถให้บริการในช่วงเวลานี้",
)


def _eligibility_error_response(exc: Exception):
    message = str(exc)
    status_code = 409 if message in _ELIGIBILITY_ERROR_MESSAGES else 400
    return jsonify({"error": message}), status_code


# ระบบยกเลิก/ขอเลื่อนนัดใช้ exception type คุมสถานะ HTTP:
#   LookupError    -> 404 (ไม่พบ)
#   PermissionError-> 403 (ไม่ใช่เจ้าของ)
#   ValueError     -> 409 (สถานะ/กฎทางธุรกิจไม่ยอมให้ทำ เช่น เหลือน้อยกว่า 2 วัน)
#   Exception อื่น -> ใช้ตรรกะเดิม (ข้อความ eligibility ของช่าง)
def _booking_action_error_response(exc: Exception):
    if isinstance(exc, LookupError):
        return jsonify({"error": str(exc)}), 404
    if isinstance(exc, PermissionError):
        return jsonify({"error": str(exc)}), 403
    if isinstance(exc, ValueError):
        return jsonify({"error": str(exc)}), 409
    return _eligibility_error_response(exc)


def _fmt_date(value):
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return value.strftime("%d/%m/%Y")


def _fmt_time(value):
    if value is None:
        return None
    if isinstance(value, _dt.timedelta):
        total_seconds = int(value.total_seconds())
        hours, remainder = divmod(total_seconds, 3600)
        minutes = remainder // 60
        return f"{hours:02d}:{minutes:02d}"
    if isinstance(value, _dt.time):
        return value.strftime("%H:%M")
    return str(value)[:5]


def _require_booking_store_or_customer_owner(booking_id):
    """ผ่านถ้าเป็นเจ้าของร้านของ booking นี้, ลูกค้าเจ้าของ booking นี้เอง, หรือช่างที่ถูก
    มอบหมายให้ดูแล booking นี้ (ดูรายละเอียด/คำขอเลื่อนนัดของคิวตัวเองได้)"""
    current = getattr(g, "current_user", None)
    if not current:
        return jsonify({"error": "Unauthorized"}), 401

    booking = get_booking_by_id(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if booking["store_id"] in current["owned_store_ids"]:
        return None
    if booking["user_id"] == current["user_id"]:
        return None
    if current["role_id"] == 3 and current["employee_id"] == booking["employee_id"]:
        return None

    return jsonify({"error": "Access denied"}), 403


def _require_booking_store_owner_or_assigned_staff(booking_id):
    """ผ่านถ้าเป็นเจ้าของร้านของ booking นี้ หรือช่างที่ถูกมอบหมายให้ดูแล booking นี้เอง
    (ไม่รวมลูกค้า) -- ใช้กับ endpoint ที่อนุญาตให้ช่างจัดการคิวของตัวเองได้ เช่น
    อนุมัติ/ยกเลิก, ขอเลื่อนนัด, ทบทวนคำขอเลื่อนนัดที่ลูกค้าส่งมา"""
    current = getattr(g, "current_user", None)
    if not current:
        return jsonify({"error": "Unauthorized"}), 401

    booking = get_booking_by_id(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if booking["store_id"] in current["owned_store_ids"]:
        return None
    if current["role_id"] == 3 and current["employee_id"] == booking["employee_id"]:
        return None

    return jsonify({"error": "Access denied"}), 403


def _require_store_view_access(store_id):
    """Admin ของร้านนี้ดูได้ทั้งหมด, ช่างของร้านนี้ดูได้ (ผลลัพธ์จะถูกกรองเหลือ
    แค่แถวของตัวเองที่ชั้น service). คืน (only_employee_id, guard)"""
    current = g.current_user

    if current["role_id"] == 2:
        if int(store_id) not in current["owned_store_ids"]:
            return None, (jsonify({"error": "Access denied: not the owner of this store"}), 403)
        return None, None

    if current["role_id"] == 3:
        if current["employee_store_id"] != int(store_id):
            return None, (jsonify({"error": "Access denied"}), 403)
        return current["employee_id"], None

    return None, (jsonify({"error": "Access denied"}), 403)


# ============================================================
#   GET /booking (list all)
# ============================================================
@booking_bp.route("/booking", methods=["GET"])
def list_booking():
    rows = get_all_booking()
    return jsonify(rows), 200


# ============================================================
#   POST /booking (create)
# ============================================================
@booking_bp.route("/booking", methods=["POST"])
def create_booking():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = [
        "booking_date",
        "booking_time",
        "user_id",
        "store_id",
        "services",
        "customer",
        "total_price",
        "total_minutes",
        "type_booking_id",
        "status_booking_id",
    ]

    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:

        # insert_booking ตรวจสอบ eligibility + คิวชน + บันทึก booking_services
        # ให้ครบในธุรกรรมเดียวแล้ว (ไม่ต้องเรียก insert_booking_services แยกอีก)
        booking_id = insert_booking(data)

        return jsonify({
            "message": "Booking created successfully",
            "booking_id": booking_id
        }), 201

    except Exception as e:

        print("BOOKING ERROR:", str(e))

        return _eligibility_error_response(e)

# ============================================================
#   GET /booking/<id>
# ============================================================
@booking_bp.route("/booking/<int:bid>", methods=["GET"])
def get_booking(bid: int):
    row = get_booking_by_id(bid)
    if not row:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify(row), 200


# ============================================================
#   PUT /booking/<id>
# ============================================================
@booking_bp.route("/booking/<int:bid>", methods=["PUT"])
@token_required
def update_booking_route(bid: int):
    guard = require_booking_store_owner(bid)
    if guard:
        return guard

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    try:
        updated = update_booking(bid, data)
    except Exception as e:
        print("BOOKING UPDATE ERROR:", str(e))
        return _eligibility_error_response(e)

    if not updated:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify({
        "message": "Booking updated successfully",
        "booking_id": bid
    }), 200


# ============================================================
#   DELETE /booking/<id>
# ============================================================
@booking_bp.route("/booking/<int:bid>", methods=["DELETE"])
@token_required
def delete_booking_route(bid: int):
    guard = require_booking_store_owner(bid)
    if guard:
        return guard

    deleted = delete_booking(bid)

    if not deleted:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify({"message": "Booking deleted"}), 200


# ============================================================
#   GET /booking/<id>/detail
# ============================================================
@booking_bp.route("/booking/<int:bid>/detail", methods=["GET"])
@token_required
def get_booking_detail(bid: int):
    guard = _require_booking_store_or_customer_owner(bid)
    if guard:
        return guard

    rows = get_booking_with_services(bid)

    if not rows:
        return jsonify({"error": "Booking not found"}), 404

    # เพิ่ม cancellable (คำนวณจากเวลาปัจจุบันฝั่ง Backend เท่านั้น) ให้ทุกแถวเหมือนกัน
    # เพื่อให้ Frontend ไม่ต้องคำนวณกฎ 2 วันเอง
    cancellable, days_until = compute_cancel_eligibility(rows[0]["booking_date_iso"])
    for row in rows:
        row["cancellable"] = cancellable
        row["days_until_booking"] = days_until

    return jsonify(rows), 200




# ============================================================
#   GET /booking/user/<user_id> (ดึงการจองของผู้ใช้โดยระบุ user_id)
#   ต้องเป็นเจ้าของ user_id นี้เท่านั้น (กันไม่ให้ query booking ของคนอื่นได้)
# ============================================================
@booking_bp.route("/booking/user/<int:user_id>", methods=["GET"])
@token_required
def list_user_bookings(user_id: int):
    guard = require_self_user(user_id)
    if guard:
        return guard

    rows = get_user_bookings(user_id)
    return jsonify(rows), 200



# ============================================================
#   GET /booking/store/<store_id>
# ============================================================
@booking_bp.route("/booking/store/<int:store_id>", methods=["GET"])
@token_required
def list_store_bookings(store_id: int):
    only_employee_id, guard = _require_store_view_access(store_id)
    if guard:
        return guard

    rows = get_store_bookings(store_id, only_employee_id=only_employee_id)
    return jsonify(rows), 200


@booking_bp.route("/bookings/<int:id>/status", methods=["PUT"])
@token_required
def update_booking_status(id):
    guard = _require_booking_store_owner_or_assigned_staff(id)
    if guard:
        return guard

    data = request.get_json(silent=True)

    if not data or "status_booking_id" not in data:
        return jsonify({"error": "Missing status_booking_id"}), 400

    new_status_id = data["status_booking_id"]
    booking = get_booking_by_id(id)

    updated = update_booking_status_service(id, new_status_id)

    if not updated:
        return jsonify({"error": "Booking not found"}), 404

    # แจ้งเตือนลูกค้าเมื่อร้านยืนยัน/ยกเลิกการจอง (ผ่านปุ่มเดิมของฝั่งร้าน)
    if booking:
        store_owner = get_store_owner_user_id(booking["store_id"])
        store_name = store_owner["store_name"] if store_owner else "ร้าน"

        if new_status_id == 2:
            create_notification(
                booking["user_id"], id, "BOOKING_CONFIRMED",
                "ร้านยืนยันการจองของคุณแล้ว",
                f"ร้าน {store_name} ยืนยันการจองของคุณแล้ว วันที่ {_fmt_date(booking['booking_date'])} "
                f"เวลา {_fmt_time(booking['booking_time'])}"
            )
        elif new_status_id == 4:
            mark_cancelled_by_store(id, data.get("reason"))
            message = f"ร้าน {store_name} ยกเลิกการจองของคุณ"
            if data.get("reason"):
                message += f" เหตุผล: {data['reason']}"
            create_notification(booking["user_id"], id, "BOOKING_CANCELLED", "ร้านยกเลิกการจองของคุณ", message)

    return jsonify({"message": "Status updated successfully"}), 200


@booking_bp.route("/booking/alerts/<int:store_id>", methods=["GET"])
@token_required
def alerts_route(store_id: int):
    guard = require_store_owner(store_id)
    if guard:
        return guard

    rows = get_recent_alerts_by_store(store_id)
    return jsonify(rows), 200


# ============================================================
#   GET /schedule/<store_id>/<date>
# ============================================================
@booking_bp.route("/schedule/<int:store_id>/<date>", methods=["GET"])
@token_required
def get_schedule_route(store_id, date):
    only_employee_id, guard = _require_store_view_access(store_id)
    if guard:
        return guard

    rows = get_schedule_from_bookings(store_id, date, only_employee_id=only_employee_id)
    return jsonify(rows), 200


# ============================================================
#   GET /schedule/<store_id>/month/<year>/<month>/summary
#   (จำนวนคิวต่อวันในเดือนนั้น -- ใช้ทำจุด indicator บนปฏิทิน)
# ============================================================
@booking_bp.route("/schedule/<int:store_id>/month/<int:year>/<int:month>/summary", methods=["GET"])
@token_required
def get_schedule_month_summary_route(store_id, year, month):
    only_employee_id, guard = _require_store_view_access(store_id)
    if guard:
        return guard

    rows = get_schedule_days_for_month(store_id, year, month, only_employee_id=only_employee_id)
    return jsonify(rows), 200




# ============================================================
#   PUT /booking/<id>/assign  (เปลี่ยน/กำหนดช่างให้คิว -- ตรวจ eligibility เต็ม
#   รูปแบบก่อนบันทึกจริง + เขียนประวัติการเปลี่ยนช่างเสมอ)
# ============================================================
@booking_bp.route("/booking/<int:booking_id>/assign", methods=["PUT"])
@token_required
def assign_employee(booking_id):
    guard = require_booking_store_owner(booking_id)
    if guard:
        return guard

    data = request.get_json(silent=True) or {}

    employee_id = data.get("employee_id")

    if not employee_id:
        return jsonify({"error": "employee_id required"}), 400

    reason = data.get("reason") or "ADMIN_CHANGE"

    try:
        reassign_booking_staff(booking_id, employee_id, reason, data.get("changed_by"))
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except Exception as e:
        print("ASSIGN ERROR:", str(e))
        return _eligibility_error_response(e)

    return jsonify({"message": "Employee assigned"}), 200


# ============================================================
#   POST /booking/<id>/random-reassign  (ช่างเดิมขาดงาน/ลา -> สุ่มช่างใหม่)
# ============================================================
@booking_bp.route("/booking/<int:booking_id>/random-reassign", methods=["POST"])
@token_required
def random_reassign_route(booking_id):
    guard = require_booking_store_owner(booking_id)
    if guard:
        return guard

    data = request.get_json(silent=True) or {}
    reason = data.get("reason") or "STAFF_ABSENT"

    try:
        picked = random_reassign_booking_staff(booking_id, reason, data.get("changed_by"))
    except LookupError as e:
        return jsonify({"error": str(e)}), 404

    if not picked:
        return jsonify({
            "eligible": False,
            "message": "ไม่พบช่างที่สามารถให้บริการในช่วงเวลานี้"
        }), 409

    return jsonify({
        "message": "Random reassign success",
        "employee_id": picked["employee_id"]
    }), 200


# ============================================================
#   GET /booking/<id>/history  (ประวัติการเปลี่ยนช่างของคิวนี้)
# ============================================================
@booking_bp.route("/booking/<int:bid>/history", methods=["GET"])
@token_required
def booking_history_route(bid):
    guard = require_booking_store_owner(bid)
    if guard:
        return guard

    rows = get_booking_staff_history(bid)
    return jsonify(rows), 200


# ============================================================
#   GET /booking/employee/<employee_id>/<date>/affected
#   (คิวของช่างคนนี้ในวันนี้ที่ได้รับผลกระทบจากการลา/ขาดงาน)
# ============================================================
@booking_bp.route("/booking/employee/<int:employee_id>/<date>/affected", methods=["GET"])
@token_required
def affected_bookings_route(employee_id, date):
    guard = require_employee_access(employee_id, write=True)
    if guard:
        return guard

    rows = get_affected_bookings_for_employee(employee_id, date)
    return jsonify({
        "affected_count": len(rows),
        "affected_bookings": rows,
        "remediation_options": ["reassign", "random_pick", "reschedule", "change_service", "cancel"],
    }), 200


# ============================================================
#   GET /booking/store/<store_id>/affected?date=YYYY-MM-DD
#   (สรุปคิวที่ได้รับผลกระทบทั้งร้าน ในวันนั้น -- ใช้กับ Dashboard)
# ============================================================
@booking_bp.route("/booking/store/<int:store_id>/affected", methods=["GET"])
@token_required
def affected_bookings_store_route(store_id):
    guard = require_store_owner(store_id)
    if guard:
        return guard

    target_date = request.args.get("date") or str(bangkok_today())
    rows = get_affected_bookings_for_store(store_id, target_date)
    return jsonify({
        "affected_count": len(rows),
        "affected_bookings": rows,
    }), 200


# ============================================================
#   PUT /booking/<id>/services  (เปลี่ยนบริการของคิว)
# ============================================================
@booking_bp.route("/booking/<int:booking_id>/services", methods=["PUT"])
@token_required
def update_booking_services_route(booking_id):
    guard = require_booking_store_owner(booking_id)
    if guard:
        return guard

    data = request.get_json(silent=True) or {}
    services = data.get("services")

    if not services:
        return jsonify({"error": "services required"}), 400

    try:
        result = replace_booking_services(booking_id, services)
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "message": "Services updated",
        "employee_unassigned": result["employee_unassigned"],
    }), 200


# ============================================================
#   GET /booking/employee/<employee_id>/<date>
# ============================================================
@booking_bp.route("/booking/employee/<int:employee_id>/<date>", methods=["GET"])
@token_required
def get_employee_schedule(employee_id, date):
    guard = require_employee_access(employee_id, write=False)
    if guard:
        return guard

    rows = get_employee_booked_times(employee_id, date)

    return jsonify(rows), 200


# ============================================================
#   POST /booking/<id>/cancel  (ลูกค้ายกเลิกการจองของตัวเอง)
#   บังคับกฎ "ยกเลิกได้ก่อนวันนัดอย่างน้อย 2 วัน" ที่ Backend เท่านั้น
# ============================================================
@booking_bp.route("/booking/<int:bid>/cancel", methods=["POST"])
@token_required
def cancel_booking_route(bid: int):
    guard = require_booking_customer_owner(bid)
    if guard:
        return guard

    data = request.get_json(silent=True) or {}
    reason = data.get("reason")

    try:
        booking = cancel_booking_by_customer(bid, g.current_user["user_id"], reason)
    except Exception as e:
        return _booking_action_error_response(e)

    store_owner = get_store_owner_user_id(booking["store_id"])
    if store_owner:
        create_notification(
            store_owner["user_id"], bid, "BOOKING_CANCELLED",
            f"ลูกค้ายกเลิกการจอง #{bid}",
            f"ลูกค้าได้ยกเลิกการจอง #{bid} สำหรับวันที่ {_fmt_date(booking['booking_date'])} "
            f"เวลา {_fmt_time(booking['booking_time'])}"
        )

    return jsonify({"message": "Booking cancelled successfully", "booking_id": bid}), 200


# ============================================================
#   POST /booking/<id>/reschedule-request  (ลูกค้าขอเลื่อนนัด)
# ============================================================
@booking_bp.route("/booking/<int:bid>/reschedule-request", methods=["POST"])
@token_required
def create_customer_reschedule_request_route(bid: int):
    guard = require_booking_customer_owner(bid)
    if guard:
        return guard

    data = request.get_json(silent=True) or {}
    proposed_date = data.get("proposed_date")
    proposed_time = data.get("proposed_time")
    reason = data.get("reason")

    if not proposed_date or not proposed_time:
        return jsonify({"error": "proposed_date and proposed_time required"}), 400

    try:
        result = create_reschedule_request(
            bid, "customer", g.current_user["user_id"], proposed_date, proposed_time, reason
        )
    except Exception as e:
        return _booking_action_error_response(e)

    store_owner = get_store_owner_user_id(result["booking"]["store_id"])
    if store_owner:
        create_notification(
            store_owner["user_id"], bid, "RESCHEDULE_REQUESTED",
            "ลูกค้าขอเลื่อนนัด",
            f"ลูกค้าขอเลื่อนนัดการจอง #{bid} เป็นวันที่ {_fmt_date(proposed_date)} "
            f"เวลา {_fmt_time(proposed_time)}"
        )

    return jsonify({
        "message": "Reschedule request created",
        "request_id": result["request_id"],
    }), 201


# ============================================================
#   POST /booking/<id>/store-reschedule  (ร้านขอเลื่อนนัดให้ลูกค้า)
# ============================================================
@booking_bp.route("/booking/<int:bid>/store-reschedule", methods=["POST"])
@token_required
def create_store_reschedule_request_route(bid: int):
    guard = _require_booking_store_owner_or_assigned_staff(bid)
    if guard:
        return guard

    data = request.get_json(silent=True) or {}
    proposed_date = data.get("proposed_date")
    proposed_time = data.get("proposed_time")
    reason = data.get("reason")

    if not proposed_date or not proposed_time:
        return jsonify({"error": "proposed_date and proposed_time required"}), 400

    try:
        result = create_reschedule_request(
            bid, "store", g.current_user["user_id"], proposed_date, proposed_time, reason
        )
    except Exception as e:
        return _booking_action_error_response(e)

    booking = result["booking"]
    create_notification(
        booking["user_id"], bid, "STORE_RESCHEDULE_PROPOSED",
        "ร้านขอเลื่อนนัดของคุณ",
        f"ร้านขอเลื่อนนัดการจอง #{bid} เป็นวันที่ {_fmt_date(proposed_date)} "
        f"เวลา {_fmt_time(proposed_time)}" + (f" เหตุผล: {reason}" if reason else "")
    )

    return jsonify({
        "message": "Store reschedule request created",
        "request_id": result["request_id"],
    }), 201


# ============================================================
#   GET /booking/<id>/reschedule-request  (คำขอล่าสุดของ booking นี้)
# ============================================================
@booking_bp.route("/booking/<int:bid>/reschedule-request", methods=["GET"])
@token_required
def get_booking_reschedule_request_route(bid: int):
    guard = _require_booking_store_or_customer_owner(bid)
    if guard:
        return guard

    row = get_latest_request_for_booking(bid)
    if not row:
        return jsonify(None), 200

    return jsonify(row), 200


def _resolve_request_booking_guard(request_id, guard_fn):
    """โหลด booking_id จาก request แล้วตรวจสิทธิ์ด้วย guard_fn คืน (booking_id, guard_response_or_None)"""
    req = get_reschedule_request_by_id(request_id)
    if not req:
        return None, (jsonify({"error": "Reschedule request not found"}), 404)
    guard = guard_fn(req["booking_id"])
    return req["booking_id"], guard


# ============================================================
#   PUT /reschedule-requests/<id>/approve  (ร้านอนุมัติคำขอที่ลูกค้าส่งมา)
# ============================================================
@booking_bp.route("/reschedule-requests/<int:request_id>/approve", methods=["PUT"])
@token_required
def approve_reschedule_request_route(request_id: int):
    booking_id, guard = _resolve_request_booking_guard(request_id, _require_booking_store_owner_or_assigned_staff)
    if guard:
        return guard

    try:
        result = approve_reschedule_request(request_id, g.current_user["user_id"])
    except Exception as e:
        return _booking_action_error_response(e)

    booking = result["booking"]
    request_row = result["request"]
    create_notification(
        booking["user_id"], booking_id, "RESCHEDULE_APPROVED",
        "ร้านยืนยันการเลื่อนนัดของคุณแล้ว",
        f"ร้านยืนยันการเลื่อนนัดของคุณแล้ว วันนัดใหม่ {_fmt_date(request_row['proposed_date'])} "
        f"เวลา {_fmt_time(request_row['proposed_time'])}"
    )

    return jsonify({"message": "Reschedule approved", "booking_id": booking_id}), 200


# ============================================================
#   PUT /reschedule-requests/<id>/reject  (ร้านปฏิเสธคำขอที่ลูกค้าส่งมา)
# ============================================================
@booking_bp.route("/reschedule-requests/<int:request_id>/reject", methods=["PUT"])
@token_required
def reject_reschedule_request_route(request_id: int):
    booking_id, guard = _resolve_request_booking_guard(request_id, _require_booking_store_owner_or_assigned_staff)
    if guard:
        return guard

    data = request.get_json(silent=True) or {}
    response_note = data.get("response_note")

    try:
        result = reject_reschedule_request(request_id, g.current_user["user_id"], response_note)
    except Exception as e:
        return _booking_action_error_response(e)

    booking = result["booking"]
    message = "ร้านไม่สามารถรับคำขอเลื่อนนัดของคุณได้ กรุณาติดต่อร้านหากต้องการเปลี่ยนแปลงการจอง"
    if response_note:
        message += f" เหตุผล: {response_note}"

    create_notification(
        booking["user_id"], booking_id, "RESCHEDULE_REJECTED",
        "ร้านไม่สามารถรับคำขอเลื่อนนัดของคุณได้", message
    )

    return jsonify({"message": "Reschedule rejected", "booking_id": booking_id}), 200


# ============================================================
#   PUT /reschedule-requests/<id>/respond  (ลูกค้าตอบรับ/ปฏิเสธคำขอที่ร้านเสนอ)
# ============================================================
@booking_bp.route("/reschedule-requests/<int:request_id>/respond", methods=["PUT"])
@token_required
def respond_to_store_reschedule_route(request_id: int):
    booking_id, guard = _resolve_request_booking_guard(request_id, require_booking_customer_owner)
    if guard:
        return guard

    data = request.get_json(silent=True) or {}
    accept = bool(data.get("accept"))
    response_note = data.get("response_note")

    try:
        result = respond_to_store_reschedule(
            request_id, g.current_user["user_id"], accept, response_note
        )
    except Exception as e:
        return _booking_action_error_response(e)

    booking = result["booking"]
    request_row = result["request"]
    store_owner = get_store_owner_user_id(booking["store_id"])
    if store_owner:
        if accept:
            create_notification(
                store_owner["user_id"], booking_id, "RESCHEDULE_APPROVED",
                "ลูกค้ายอมรับการเลื่อนนัด",
                f"ลูกค้ายอมรับการเลื่อนนัดการจอง #{booking_id} เป็นวันที่ "
                f"{_fmt_date(request_row['proposed_date'])} เวลา {_fmt_time(request_row['proposed_time'])}"
            )
        else:
            create_notification(
                store_owner["user_id"], booking_id, "RESCHEDULE_REJECTED",
                "ลูกค้าปฏิเสธการเลื่อนนัด",
                f"ลูกค้าปฏิเสธการเลื่อนนัดที่ร้านเสนอสำหรับการจอง #{booking_id}"
            )

    return jsonify({
        "message": "Reschedule accepted" if accept else "Reschedule rejected",
        "booking_id": booking_id,
    }), 200
