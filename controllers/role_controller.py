from flask import Blueprint, request, jsonify
from services.role_service import (
    get_all_role,
    get_role_by_id,
    insert_role,
    update_role,
    delete_role,
)

role_bp = Blueprint("role", __name__, url_prefix="/role")

# ============================================================
#   GET /role (list all) + POST /role (create)
# ============================================================
@role_bp.route("/role", methods=["GET"])
def list_role():
    rows = get_all_role()
    return jsonify(rows), 200


@role_bp.route("/role", methods=["POST"])
def create_role():
    """เพิ่ม role ใหม่ลงฐานข้อมูล"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["role_name", "description"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    role_name = data["role_name"]
    description = data["description"]

    new_id = insert_role(role_name, description)

    return jsonify({
        "message": "Role created successfully",
        "role_id": new_id
    }), 201


# ============================================================
# GET /role/<id>  |  PUT /role/<id>  |  DELETE /role/<id>
# ============================================================
@role_bp.route("/role/<int:rid>", methods=["GET"])
def get_role(rid: int):
    row = get_role_by_id(rid)
    if not row:
        return jsonify({"error": "Role not found"}), 404
    return jsonify(row), 200


@role_bp.route("/role/<int:rid>", methods=["PUT"])
def update_role_route(rid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_role(rid, data)

    if not updated:
        return jsonify({"error": "Role not found"}), 404

    return jsonify({
        "message": "Role updated successfully",
        "role_id": rid
    }), 200


@role_bp.route("/role/<int:rid>", methods=["DELETE"])
def delete_role_route(rid: int):
    deleted = delete_role(rid)

    if not deleted:
        return jsonify({"error": "Role not found"}), 404

    return jsonify({"message": "Role deleted"}), 200
