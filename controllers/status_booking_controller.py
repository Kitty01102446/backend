from flask import Blueprint, request, jsonify
from services.status_booking_service import (
    get_all_status_booking,
    get_status_booking_by_id,
    insert_status_booking,
    update_status_booking,
    delete_status_booking,
)

status_booking_bp = Blueprint("status_booking", __name__, url_prefix="/status_booking")

# ============================================================
#   GET /status_booking (list all) + POST /status_booking (create)
# ============================================================
@status_booking_bp.route("/status_booking", methods=["GET"])
def list_status_booking():
    rows = get_all_status_booking()
    return jsonify(rows), 200


@status_booking_bp.route("/status_booking", methods=["POST"])
def create_status_booking():
    """เพิ่ม status_booking ใหม่"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["status_booking_name"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    status_booking_name = data["status_booking_name"]
    description = data.get("description", "")

    new_id = insert_status_booking(status_booking_name, description)

    return jsonify({
        "message": "Status Booking created successfully",
        "status_booking_id": new_id
    }), 201


# ============================================================
# GET /status_booking/<id> | PUT /status_booking/<id> | DELETE /status_booking/<id>
# ============================================================
@status_booking_bp.route("/status_booking/<int:sid>", methods=["GET"])
def get_status_booking(sid: int):
    row = get_status_booking_by_id(sid)
    if not row:
        return jsonify({"error": "Status Booking not found"}), 404
    return jsonify(row), 200


@status_booking_bp.route("/status_booking/<int:sid>", methods=["PUT"])
def update_status_booking_route(sid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_status_booking(sid, data)

    if not updated:
        return jsonify({"error": "Status Booking not found"}), 404

    return jsonify({
        "message": "Status Booking updated successfully",
        "status_booking_id": sid
    }), 200


@status_booking_bp.route("/status_booking/<int:sid>", methods=["DELETE"])
def delete_status_booking_route(sid: int):
    deleted = delete_status_booking(sid)

    if not deleted:
        return jsonify({"error": "Status Booking not found"}), 404

    return jsonify({"message": "Status Booking deleted"}), 200
