"""
ข้อร้องเรียน -- ลูกค้า/เจ้าของร้านที่ login แล้ว (role ใดก็ได้) แจ้งเรื่องเข้ามาได้
(POST /complaints) ส่วนดู/ตัดสินเป็นสิทธิ์ผู้ดูแลระบบเท่านั้น (/admin/complaints/*)
"""

from flask import Blueprint, request, jsonify, g

from services.auth_service import token_required, require_admin
from services.complaint_service import (
    create_complaint,
    list_complaints,
    get_complaint_by_id,
    resolve_complaint,
)

complaint_bp = Blueprint("complaint_bp", __name__)


@complaint_bp.route("/complaints", methods=["POST"])
@token_required
def create_complaint_route():
    data = request.get_json(silent=True) or {}
    subject = data.get("subject")
    detail = data.get("detail")
    if not subject or not detail:
        return jsonify({"error": "Missing subject or detail"}), 400

    new_id = create_complaint(
        reporter_user_id=g.current_user["user_id"],
        subject=subject,
        detail=detail,
        booking_id=data.get("booking_id"),
        against_store_id=data.get("against_store_id"),
    )
    return jsonify({"message": "Complaint submitted", "complaint_id": new_id}), 201


@complaint_bp.route("/admin/complaints", methods=["GET"])
@token_required
def list_complaints_route():
    guard = require_admin()
    if guard:
        return guard
    status = request.args.get("status")
    return jsonify(list_complaints(status)), 200


@complaint_bp.route("/admin/complaints/<int:complaint_id>", methods=["GET"])
@token_required
def get_complaint_route(complaint_id):
    guard = require_admin()
    if guard:
        return guard
    row = get_complaint_by_id(complaint_id)
    if not row:
        return jsonify({"error": "Complaint not found"}), 404
    return jsonify(row), 200


@complaint_bp.route("/admin/complaints/<int:complaint_id>/resolve", methods=["PUT"])
@token_required
def resolve_complaint_route(complaint_id):
    guard = require_admin()
    if guard:
        return guard
    data = request.get_json(silent=True) or {}
    status = data.get("status")
    note = data.get("resolution_note", "")
    if status not in ("RESOLVED", "REJECTED", "IN_REVIEW"):
        return jsonify({"error": "status must be RESOLVED, REJECTED or IN_REVIEW"}), 400

    updated = resolve_complaint(complaint_id, status, note, g.current_user["user_id"])
    if not updated:
        return jsonify({"error": "Complaint not found"}), 404
    return jsonify({"message": "Complaint updated"}), 200
