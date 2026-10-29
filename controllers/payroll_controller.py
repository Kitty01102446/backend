"""
ระบบเงินเดือน (เฟส 2)

โครงสร้างค่าจ้าง = เงินเดือนฐาน + คอมมิชชั่น (ดู payroll_service.py) ทุก endpoint
ต้อง login และตรวจสิทธิ์ตาม role: Admin (เจ้าของร้าน) จัดการ/ดูได้ทุกคนในร้านตัวเอง,
ช่าง (Staff) ดูได้เฉพาะของตัวเอง (ห้ามแก้ไข/ยืนยันเงินเดือน -- เป็นสิทธิ์ของ Admin
เท่านั้น)
"""

from flask import Blueprint, request, jsonify

from services.employee_service import get_employee_by_id
from services.payroll_service import (
    set_employee_pay_rate,
    compute_draft_payroll,
    get_store_payroll,
    confirm_payroll,
    get_employee_payroll_history,
)
from services.timeutil import bangkok_now
from services.auth_service import token_required, require_store_owner, require_employee_access

payroll_bp = Blueprint("payroll_bp", __name__)


def _current_period():
    now = bangkok_now()
    return now.year, now.month


# ============================================================
#   PUT /employees/<id>/pay-rate  (ตั้ง/แก้เงินเดือนฐาน + % คอมมิชชั่น)
# ============================================================
@payroll_bp.route("/employees/<int:employee_id>/pay-rate", methods=["PUT"])
@token_required
def update_pay_rate(employee_id):
    guard = require_employee_access(employee_id, write=True)
    if guard:
        return guard

    if not get_employee_by_id(employee_id):
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True) or {}
    updated = set_employee_pay_rate(
        employee_id, data.get("base_salary"), data.get("commission_rate")
    )
    if not updated:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({"message": "Pay rate updated"}), 200


# ============================================================
#   GET /employees/<id>/payroll?year=&month=  (ร่างเงินเดือนของงวดนั้น)
# ============================================================
@payroll_bp.route("/employees/<int:employee_id>/payroll", methods=["GET"])
@token_required
def get_employee_payroll(employee_id):
    guard = require_employee_access(employee_id, write=False)
    if guard:
        return guard

    if not get_employee_by_id(employee_id):
        return jsonify({"error": "Employee not found"}), 404

    default_year, default_month = _current_period()
    year = int(request.args.get("year", default_year))
    month = int(request.args.get("month", default_month))

    try:
        record = compute_draft_payroll(employee_id, year, month)
    except LookupError as e:
        return jsonify({"error": str(e)}), 404

    return jsonify(record), 200


# ============================================================
#   GET /employees/<id>/payroll/history
# ============================================================
@payroll_bp.route("/employees/<int:employee_id>/payroll/history", methods=["GET"])
@token_required
def payroll_history(employee_id):
    guard = require_employee_access(employee_id, write=False)
    if guard:
        return guard

    rows = get_employee_payroll_history(employee_id)
    return jsonify(rows), 200


# ============================================================
#   POST /employees/<id>/payroll/confirm
# ============================================================
@payroll_bp.route("/employees/<int:employee_id>/payroll/confirm", methods=["POST"])
@token_required
def confirm_employee_payroll(employee_id):
    guard = require_employee_access(employee_id, write=True)
    if guard:
        return guard

    if not get_employee_by_id(employee_id):
        return jsonify({"error": "Employee not found"}), 404

    data = request.get_json(silent=True) or {}
    default_year, default_month = _current_period()
    year = int(data.get("year", default_year))
    month = int(data.get("month", default_month))

    updated = confirm_payroll(
        employee_id, year, month,
        confirmed_by=data.get("confirmed_by"),
        total_amount_override=data.get("total_amount"),
    )
    if not updated:
        return jsonify({"error": "Confirm failed"}), 400

    return jsonify({"message": "Payroll confirmed"}), 200


# ============================================================
#   GET /employees/store/<store_id>/payroll?year=&month=
#   (สรุปเงินเดือนพนักงานทุกคนในร้าน สำหรับงวดนั้น)
# ============================================================
@payroll_bp.route("/employees/store/<int:store_id>/payroll", methods=["GET"])
@token_required
def store_payroll(store_id):
    guard = require_store_owner(store_id)
    if guard:
        return guard

    default_year, default_month = _current_period()
    year = int(request.args.get("year", default_year))
    month = int(request.args.get("month", default_month))

    rows = get_store_payroll(store_id, year, month)
    return jsonify(rows), 200
