from flask import Blueprint, request, jsonify
from services.type_booking_service import (
    get_all_type_bookings,
    get_type_booking_by_id,
    insert_type_booking,
    update_type_booking,
    delete_type_booking,
)

type_booking_bp = Blueprint("type_booking", __name__, url_prefix="/type_booking")

# ============================================================
#   GET /type_booking  +  POST /type_booking
# ============================================================
@type_booking_bp.route("/type_booking", methods=["GET"])
def list_type_bookings():
    rows = get_all_type_bookings()
    return jsonify(rows), 200


@type_booking_bp.route("/type_booking", methods=["POST"])
def create_type_booking():
    """เพิ่มข้อมูลประเภทการจอง"""

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["type_booking_name", "description"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    type_booking_name = data["type_booking_name"]
    description = data["description"]

    new_id = insert_type_booking(
        type_booking_name=type_booking_name,
        description=description
    )

    return jsonify({
        "message": "Type Booking created successfully",
        "type_booking_id": new_id
    }), 201


# ============================================================
#   GET /type_booking/<id>
#   PUT /type_booking/<id>
#   DELETE /type_booking/<id>
# ============================================================
@type_booking_bp.route("/type_booking/<int:tid>", methods=["GET"])
def get_type_booking(tid: int):
    row = get_type_booking_by_id(tid)
    if not row:
        return jsonify({"error": "Type Booking not found"}), 404
    return jsonify(row), 200


@type_booking_bp.route("/type_booking/<int:tid>", methods=["PUT"])
def update_type_booking_route(tid: int):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_type_booking(tid, data)
    if not updated:
        return jsonify({"error": "Type Booking not found"}), 404

    return jsonify({
        "message": "Type Booking updated successfully",
        "type_booking_id": tid
    }), 200


@type_booking_bp.route("/type_booking/<int:tid>", methods=["DELETE"])
def delete_type_booking_route(tid: int):
    deleted = delete_type_booking(tid)
    if not deleted:
        return jsonify({"error": "Type Booking not found"}), 404

    return jsonify({"message": "Type Booking deleted"}), 200
