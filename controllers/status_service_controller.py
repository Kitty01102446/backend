from flask import Blueprint, request, jsonify
from services.status_service_service import (
    get_all_status_service,
    get_status_service_by_id,
    insert_status_service,
    update_status_service,
    delete_status_service,
)

status_service_bp = Blueprint("status_service_bp", __name__)

# ============================================================
#   GET /status_service (list all) + POST /status_service (create)
# ============================================================
@status_service_bp.route("/status_service", methods=["GET"])
def list_status_service():
    rows = get_all_status_service()
    return jsonify(rows), 200


@status_service_bp.route("/status_service", methods=["POST"])
def create_status_service():
    """เพิ่ม status_service ใหม่"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["status_service_name"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    status_service_name = data["status_service_name"]
    description = data.get("description", "")

    new_id = insert_status_service(status_service_name, description)

    return jsonify({
        "message": "Status Service created successfully",
        "status_service_id": new_id
    }), 201


# ============================================================
# GET /status_service/<id> | PUT /status_service/<id> | DELETE /status_service/<id>
# ============================================================
@status_service_bp.route("/status_service/<int:sid>", methods=["GET"])
def get_status_service(sid: int):
    row = get_status_service_by_id(sid)
    if not row:
        return jsonify({"error": "Status Service not found"}), 404
    return jsonify(row), 200


@status_service_bp.route("/status_service/<int:sid>", methods=["PUT"])
def update_status_service_route(sid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_status_service(sid, data)

    if not updated:
        return jsonify({"error": "Status Service not found"}), 404

    return jsonify({
        "message": "Status Service updated successfully",
        "status_service_id": sid
    }), 200


@status_service_bp.route("/status_service/<int:sid>", methods=["DELETE"])
def delete_status_service_route(sid: int):
    deleted = delete_status_service(sid)

    if not deleted:
        return jsonify({"error": "Status Service not found"}), 404

    return jsonify({"message": "Status Service deleted"}), 200
