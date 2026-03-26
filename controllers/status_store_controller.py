from flask import Blueprint, request, jsonify
from services.status_store_service import (
    get_all_status_store,
    get_status_store_by_id,
    insert_status_store,
    update_status_store,
    delete_status_store,
)

status_store_bp = Blueprint("status_store_bp", __name__)

# ============================================================
#   GET /status_store (list all) + POST /status_store (create)
# ============================================================
@status_store_bp.route("/status_store", methods=["GET"])
def list_status_store():
    rows = get_all_status_store()
    return jsonify(rows), 200


@status_store_bp.route("/status_store", methods=["POST"])
def create_status_store():
    """เพิ่ม status_store ใหม่ลงฐานข้อมูล"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["status_store_name"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    status_store_name = data["status_store_name"]
    description = data.get("description", "")

    new_id = insert_status_store(status_store_name, description)

    return jsonify({
        "message": "Status Store created successfully",
        "status_store_id": new_id
    }), 201


# ============================================================
# GET /status_store/<id> | PUT /status_store/<id> | DELETE /status_store/<id>
# ============================================================
@status_store_bp.route("/status_store/<int:sid>", methods=["GET"])
def get_status_store(sid: int):
    row = get_status_store_by_id(sid)
    if not row:
        return jsonify({"error": "Status Store not found"}), 404
    return jsonify(row), 200


@status_store_bp.route("/status_store/<int:sid>", methods=["PUT"])
def update_status_store_route(sid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_status_store(sid, data)

    if not updated:
        return jsonify({"error": "Status Store not found"}), 404

    return jsonify({
        "message": "Status Store updated successfully",
        "status_store_id": sid
    }), 200


@status_store_bp.route("/status_store/<int:sid>", methods=["DELETE"])
def delete_status_store_route(sid: int):
    deleted = delete_status_store(sid)

    if not deleted:
        return jsonify({"error": "Status Store not found"}), 404

    return jsonify({"message": "Status Store deleted"}), 200


