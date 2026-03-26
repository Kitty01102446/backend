from flask import Blueprint, request, jsonify
from services.permission_service import (
    get_all_permission,
    get_permission_by_id,
    insert_permission,
    update_permission,
    delete_permission,
)

permission_bp = Blueprint("permission_bp", __name__)

# ============================================================
#   GET /permission (list all) + POST /permission (create)
# ============================================================
@permission_bp.route("/permission", methods=["GET"])
def list_permission():
    rows = get_all_permission()
    return jsonify(rows), 200


@permission_bp.route("/permission", methods=["POST"])
def create_permission():
    """เพิ่ม permission ใหม่ลงฐานข้อมูล"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["code", "name"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    code = data["code"]
    name = data["name"]

    new_id = insert_permission(code, name)

    return jsonify({
        "message": "Permission created successfully",
        "permission_id": new_id
    }), 201


# ============================================================
#             GET /permission/<id>
#             PUT /permission/<id>
#           DELETE /permission/<id>
# ============================================================
@permission_bp.route("/permission/<int:pid>", methods=["GET"])
def get_permission(pid: int):
    row = get_permission_by_id(pid)
    if not row:
        return jsonify({"error": "Permission not found"}), 404
    return jsonify(row), 200


@permission_bp.route("/permission/<int:pid>", methods=["PUT"])
def update_permission_route(pid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_permission(pid, data)

    if not updated:
        return jsonify({"error": "Permission not found"}), 404

    return jsonify({
        "message": "Permission updated successfully",
        "permission_id": pid
    }), 200


@permission_bp.route("/permission/<int:pid>", methods=["DELETE"])
def delete_permission_route(pid: int):
    deleted = delete_permission(pid)

    if not deleted:
        return jsonify({"error": "Permission not found"}), 404

    return jsonify({"message": "Permission deleted"}), 200
