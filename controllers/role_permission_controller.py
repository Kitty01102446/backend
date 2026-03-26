from flask import Blueprint, request, jsonify
from services.role_permission_service import (
    get_all_role_permission,
    get_role_permission_by_id,
    insert_role_permission,
    update_role_permission,
    delete_role_permission,
)

role_permission_bp = Blueprint("role_permission_bp", __name__)

# ============================================================
#   GET /role_permission (list all) + POST /role_permission (create)
# ============================================================
@role_permission_bp.route("/role_permission", methods=["GET"])
def list_role_permission():
    rows = get_all_role_permission()
    return jsonify(rows), 200


@role_permission_bp.route("/role_permission", methods=["POST"])
def create_role_permission():
    """เพิ่ม role_permission ใหม่ลงฐานข้อมูล"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["permission_id", "role_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    permission_id = data["permission_id"]
    role_id = data["role_id"]

    new_id = insert_role_permission(permission_id, role_id)

    return jsonify({
        "message": "Role Permission created successfully",
        "role_permission_id": new_id
    }), 201


# ============================================================
# GET /role_permission/<id> | PUT /role_permission/<id> | DELETE /role_permission/<id>
# ============================================================
@role_permission_bp.route("/role_permission/<int:rpid>", methods=["GET"])
def get_role_permission(rpid: int):
    row = get_role_permission_by_id(rpid)
    if not row:
        return jsonify({"error": "Role Permission not found"}), 404
    return jsonify(row), 200


@role_permission_bp.route("/role_permission/<int:rpid>", methods=["PUT"])
def update_role_permission_route(rpid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_role_permission(rpid, data)

    if not updated:
        return jsonify({"error": "Role Permission not found"}), 404

    return jsonify({
        "message": "Role Permission updated successfully",
        "role_permission_id": rpid
    }), 200


@role_permission_bp.route("/role_permission/<int:rpid>", methods=["DELETE"])
def delete_role_permission_route(rpid: int):
    deleted = delete_role_permission(rpid)

    if not deleted:
        return jsonify({"error": "Role Permission not found"}), 404

    return jsonify({"message": "Role Permission deleted"}), 200
