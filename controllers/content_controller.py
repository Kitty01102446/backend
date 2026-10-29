"""
เนื้อหาหน้าเว็บ (แบนเนอร์/ข่าวสาร/ประกาศ) -- จัดการได้เฉพาะผู้ดูแลระบบ
"""

from flask import Blueprint, request, jsonify, g

from services.auth_service import token_required, require_admin
from services.content_service import (
    list_content,
    create_content,
    update_content,
    delete_content,
)

content_bp = Blueprint("content_bp", __name__)


@content_bp.route("/admin/content", methods=["GET"])
@token_required
def list_content_route():
    guard = require_admin()
    if guard:
        return guard
    content_type = request.args.get("content_type")
    return jsonify(list_content(content_type)), 200


@content_bp.route("/admin/content", methods=["POST"])
@token_required
def create_content_route():
    guard = require_admin()
    if guard:
        return guard
    data = request.get_json(silent=True) or {}
    if not data.get("content_type") or not data.get("title"):
        return jsonify({"error": "Missing content_type or title"}), 400
    new_id = create_content(data, g.current_user["user_id"])
    return jsonify({"message": "Content created", "content_id": new_id}), 201


@content_bp.route("/admin/content/<int:content_id>", methods=["PUT"])
@token_required
def update_content_route(content_id):
    guard = require_admin()
    if guard:
        return guard
    data = request.get_json(silent=True) or {}
    updated = update_content(content_id, data)
    if not updated:
        return jsonify({"error": "Content not found or no fields to update"}), 404
    return jsonify({"message": "Content updated"}), 200


@content_bp.route("/admin/content/<int:content_id>", methods=["DELETE"])
@token_required
def delete_content_route(content_id):
    guard = require_admin()
    if guard:
        return guard
    deleted = delete_content(content_id)
    if not deleted:
        return jsonify({"error": "Content not found"}), 404
    return jsonify({"message": "Content deleted"}), 200
