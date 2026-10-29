"""
สถานะพนักงาน / ทักษะ / เวลาทำงาน / การลา / การขาดงานกะทันหัน

ทุก endpoint ในไฟล์นี้ต้อง login (token_required) แล้วตรวจสิทธิ์ตาม role:
Admin (เจ้าของร้าน) จัดการ/ดูได้ทุกคนในร้านตัวเอง, ช่าง (Staff) ดูได้เฉพาะของ
ตัวเอง (ห้ามแก้ไข/สั่งงานแทนตัวเอง -- เป็นสิทธิ์ของ Admin เท่านั้น)
"""

from datetime import date
from flask import Blueprint, request, jsonify, g

from services.employee_service import get_employee_by_id
from services.employee_skill_service import get_employee_skills, set_employee_skills
from services.employee_status_service import (
    get_employee_status_today,
    set_employee_current_status,
    get_employee_work_hours,
    set_employee_work_hours,
    create_leave,
    get_employee_leaves,
    cancel_leave,
    approve_leave,
    reject_leave,
    get_pending_leaves,
    get_employee_day_status,
    set_employee_absent,
)
from services.booking_eligibility_service import get_eligible_employees
from services.timeutil import bangkok_today
from services.auth_service import token_required, require_store_owner, require_employee_access

employee_status_bp = Blueprint("employee_status_bp", __name__)


def _parse_service_ids(raw: str):
    if not raw:
        return []
    return [int(x) for x in raw.split(",") if x.strip().isdigit()]


def _require_store_view_access(store_id):
    """Admin ของร้านนี้ดูได้ทั้งหมด, ช่างของร้านนี้ดูได้ (แต่ผลลัพธ์จะถูกกรอง
    เหลือแค่แถวของตัวเองที่ชั้น service). คืน (only_employee_id, guard)"""
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
#   GET /employees/store/<store_id>/status-today
# ============================================================
@employee_status_bp.route("/employees/store/<int:store_id>/status-today", methods=["GET"])
@token_required
def status_today(store_id):
    only_employee_id, guard = _require_store_view_access(store_id)
    if guard:
        return guard

    rows = get_employee_status_today(store_id, only_employee_id=only_employee_id)
    return jsonify(rows), 200


# ============================================================
#   GET /employees/store/<store_id>/day-status?date=YYYY-MM-DD
#   (สถานะลา/ขาดงานของพนักงานทุกคน สำหรับวันที่ระบุ ไม่จำกัดแค่วันนี้ --
#   ใช้แสดง badge บนหน้าจองของลูกค้าทันทีที่เลือกวันที่ ไม่ต้องกดเลือกเวลาก่อน)
# ============================================================
@employee_status_bp.route("/employees/store/<int:store_id>/day-status", methods=["GET"])
def day_status(store_id):
    target_date = request.args.get("date")
    if not target_date:
        return jsonify({"error": "Missing date"}), 400

    # หน้าจองของลูกค้า (public) ก็ใช้ endpoint นี้อยู่ -- คงพฤติกรรมเดิมไว้
    # (public, ไม่ผูก auth) แต่ถ้ามี token แนบมาและเป็นช่าง ให้กรองเหลือแค่ตัวเอง
    from services.auth_service import get_current_user
    current = get_current_user()
    only_employee_id = current["employee_id"] if current and current["role_id"] == 3 else None

    rows = get_employee_day_status(store_id, target_date, only_employee_id=only_employee_id)
    return jsonify(rows), 200


# ============================================================
#   PUT /employees/<employee_id>/status  (Available / Working / Break / Off)
# ============================================================
@employee_status_bp.route("/employees/<int:employee_id>/status", methods=["PUT"])
@token_required
def update_status(employee_id):
    guard = require_employee_access(employee_id, write=True)
    if guard:
        return guard

    if not get_employee_by_id(employee_id):
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True) or {}
    status_employee_id = data.get("status_employee_id")

    if not status_employee_id:
        return jsonify({"error": "Missing status_employee_id"}), 400

    try:
        updated = set_employee_current_status(
            employee_id, status_employee_id, data.get("changed_by")
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    if not updated:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({"message": "Status updated"}), 200


# ============================================================
#   POST /employees/<employee_id>/absent  -- จุดเริ่ม flow ช่างขาดงานกะทันหัน
# ============================================================
@employee_status_bp.route("/employees/<int:employee_id>/absent", methods=["POST"])
@token_required
def mark_absent(employee_id):
    guard = require_employee_access(employee_id, write=True)
    if guard:
        return guard

    if not get_employee_by_id(employee_id):
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True) or {}
    absence_date = data.get("absence_date") or str(bangkok_today())

    try:
        result = set_employee_absent(
            employee_id, absence_date, data.get("reason"), data.get("changed_by")
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 409

    return jsonify({
        "message": "Employee marked absent",
        "affected_count": result["affected_count"],
        "affected_bookings": result["affected_bookings"],
    }), 201


# ============================================================
#   POST /employees/<employee_id>/leave
# ============================================================
@employee_status_bp.route("/employees/<int:employee_id>/leave", methods=["POST"])
@token_required
def request_leave(employee_id):
    # write=False ที่นี่ตั้งใจ -- แม้ endpoint นี้จะเขียนข้อมูล แต่ต้องการอนุญาตให้
    # ช่างขอลาของตัวเองได้ ไม่ใช่แค่เจ้าของร้าน (คำขอเริ่มที่ PENDING เสมอ ต้องรอ
    # อนุมัติจาก Admin จึงมีผลจริง)
    guard = require_employee_access(employee_id, write=False)
    if guard:
        return guard

    if not get_employee_by_id(employee_id):
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True) or {}
    leave_scope = data.get("leave_scope")
    absence_date = data.get("absence_date")

    if not leave_scope or not absence_date:
        return jsonify({"error": "Missing leave_scope or absence_date"}), 400

    try:
        absence_id = create_leave(
            employee_id, leave_scope, absence_date,
            data.get("start_time"), data.get("end_time"),
            data.get("reason"), data.get("changed_by"),
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({
        "message": "Leave request submitted, pending approval",
        "absence_id": absence_id,
    }), 201


# ============================================================
#   GET /employees/<employee_id>/leaves
# ============================================================
@employee_status_bp.route("/employees/<int:employee_id>/leaves", methods=["GET"])
@token_required
def list_leaves(employee_id):
    guard = require_employee_access(employee_id, write=False)
    if guard:
        return guard

    rows = get_employee_leaves(
        employee_id, request.args.get("date_from"), request.args.get("date_to")
    )
    return jsonify(rows), 200


# ============================================================
#   DELETE /employees/<employee_id>/leave/<absence_id>  (ยกเลิก/ถอนคำขอ)
# ============================================================
@employee_status_bp.route("/employees/<int:employee_id>/leave/<int:absence_id>", methods=["DELETE"])
@token_required
def delete_leave(employee_id, absence_id):
    # write=False ตั้งใจ -- ช่างยกเลิกคำขอลาของตัวเองได้ (ดู request_leave ด้านบน)
    guard = require_employee_access(employee_id, write=False)
    if guard:
        return guard

    cancelled = cancel_leave(absence_id)
    if not cancelled:
        return jsonify({"error": "Leave record not found or already cancelled"}), 404
    return jsonify({"message": "Leave cancelled"}), 200


# ============================================================
#   GET /employees/store/<store_id>/leave/pending  (รายการรออนุมัติ)
# ============================================================
@employee_status_bp.route("/employees/store/<int:store_id>/leave/pending", methods=["GET"])
@token_required
def pending_leaves(store_id):
    guard = require_store_owner(store_id)
    if guard:
        return guard

    rows = get_pending_leaves(store_id)
    return jsonify(rows), 200


# ============================================================
#   POST /employees/<employee_id>/leave/<absence_id>/approve
# ============================================================
@employee_status_bp.route("/employees/<int:employee_id>/leave/<int:absence_id>/approve", methods=["POST"])
@token_required
def approve_leave_route(employee_id, absence_id):
    guard = require_employee_access(employee_id, write=True)
    if guard:
        return guard

    data = request.get_json(silent=True) or {}
    approved = approve_leave(absence_id, data.get("approved_by"))
    if not approved:
        return jsonify({"error": "Leave request not found or not pending"}), 404
    return jsonify({"message": "Leave approved"}), 200


# ============================================================
#   POST /employees/<employee_id>/leave/<absence_id>/reject
# ============================================================
@employee_status_bp.route("/employees/<int:employee_id>/leave/<int:absence_id>/reject", methods=["POST"])
@token_required
def reject_leave_route(employee_id, absence_id):
    guard = require_employee_access(employee_id, write=True)
    if guard:
        return guard

    data = request.get_json(silent=True) or {}
    rejected = reject_leave(absence_id, data.get("rejected_by"))
    if not rejected:
        return jsonify({"error": "Leave request not found or not pending"}), 404
    return jsonify({"message": "Leave rejected"}), 200


# ============================================================
#   GET / PUT /employees/<employee_id>/work-hours
# ============================================================
@employee_status_bp.route("/employees/<int:employee_id>/work-hours", methods=["GET"])
@token_required
def work_hours_get(employee_id):
    guard = require_employee_access(employee_id, write=False)
    if guard:
        return guard

    rows = get_employee_work_hours(employee_id)
    return jsonify(rows), 200


@employee_status_bp.route("/employees/<int:employee_id>/work-hours", methods=["PUT"])
@token_required
def work_hours_put(employee_id):
    # write=False ตั้งใจ -- ช่างแก้เวลาทำงานของตัวเองได้ (ดู request_leave ด้านบน)
    guard = require_employee_access(employee_id, write=False)
    if guard:
        return guard

    if not get_employee_by_id(employee_id):
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True) or {}

    try:
        set_employee_work_hours(employee_id, data.get("hours") or [])
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

    return jsonify({"message": "Work hours updated"}), 200


# ============================================================
#   GET / PUT /employees/<employee_id>/skills
# ============================================================
@employee_status_bp.route("/employees/<int:employee_id>/skills", methods=["GET"])
@token_required
def skills_get(employee_id):
    guard = require_employee_access(employee_id, write=False)
    if guard:
        return guard

    rows = get_employee_skills(employee_id)
    return jsonify(rows), 200


@employee_status_bp.route("/employees/<int:employee_id>/skills", methods=["PUT"])
@token_required
def skills_put(employee_id):
    guard = require_employee_access(employee_id, write=True)
    if guard:
        return guard

    if not get_employee_by_id(employee_id):
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True) or {}
    service_ids = data.get("service_ids")

    if service_ids is None:
        return jsonify({"error": "Missing service_ids"}), 400

    set_employee_skills(employee_id, service_ids)
    return jsonify({"message": "Skills updated"}), 200


# ============================================================
#   GET /employees/store/<store_id>/available
# ============================================================
@employee_status_bp.route("/employees/store/<int:store_id>/available", methods=["GET"])
def available_staff(store_id):
    # public ตั้งใจ -- หน้าจองของลูกค้าต้องใช้เช็คว่าช่วงเวลาไหนมีช่างว่างบ้าง
    # ก่อนให้ลูกค้าเลือก คืนแค่ employee_id/fullname ไม่มีข้อมูลอ่อนไหว (เหมือน
    # day-status ด้านบนที่ public อยู่แล้วด้วยเหตุผลเดียวกัน)
    booking_date = request.args.get("date")
    booking_time = request.args.get("time")
    minutes = request.args.get("minutes")
    service_ids = _parse_service_ids(request.args.get("service_ids"))

    if not booking_date or not booking_time or not minutes or not service_ids:
        return jsonify({"error": "Missing date/time/minutes/service_ids"}), 400

    exclude_id = request.args.get("exclude_booking_id")
    exclude_id = int(exclude_id) if exclude_id else None

    rows = get_eligible_employees(
        store_id, booking_date, booking_time, int(minutes), service_ids,
        exclude_booking_id=exclude_id,
    )
    return jsonify(rows), 200


# ============================================================
#   GET /employees/<employee_id>/availability
# ============================================================
@employee_status_bp.route("/employees/<int:employee_id>/availability", methods=["GET"])
def employee_availability(employee_id):
    # public ตั้งใจ -- ลูกค้าเลือกช่างเองในหน้าจอง ต้องเช็คได้ว่าช่างคนนั้นว่าง
    # ช่วงเวลาที่เลือกไหม คืนแค่ {"eligible": true/false} ไม่มีข้อมูลอ่อนไหว
    emp = get_employee_by_id(employee_id)
    if not emp:
        return jsonify({"error": "Employee not found"}), 404

    booking_date = request.args.get("date")
    booking_time = request.args.get("time")
    minutes = request.args.get("minutes")
    service_ids = _parse_service_ids(request.args.get("service_ids"))

    if not booking_date or not booking_time or not minutes or not service_ids:
        return jsonify({"error": "Missing date/time/minutes/service_ids"}), 400

    exclude_id = request.args.get("exclude_booking_id")
    exclude_id = int(exclude_id) if exclude_id else None

    eligible = get_eligible_employees(
        emp["store_id"], booking_date, booking_time, int(minutes), service_ids,
        exclude_booking_id=exclude_id,
    )
    is_eligible = any(e["employee_id"] == employee_id for e in eligible)

    return jsonify({"eligible": is_eligible}), 200
