import os
import sys
from services.booking_service import get_store_bookings
from services.booking_service import (
    get_all_booking,
    get_booking_by_id,
    insert_booking,
    update_booking,
    delete_booking,
    get_booking_with_services,
    insert_booking_services,
    get_user_bookings,
    get_store_bookings,
    update_booking_status_service,
    get_recent_alerts_by_store,
    get_schedule_from_bookings,
    get_employee_booked_times
)
from flask import current_app




# ✅ บังคับให้ Python มองเห็นโฟลเดอร์หลัก (backend) 
# เพื่อให้ import services หรือ config ได้ถูกต้อง
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from flask import Blueprint, request, jsonify
# ตอนนี้ Python จะหาโฟลเดอร์ services เจอแล้ว
from services.booking_service import (
    get_all_booking,
    get_booking_by_id,
    insert_booking,
    update_booking,
    delete_booking,
    get_booking_with_services,
    insert_booking_services,
    get_user_bookings
)

booking_bp = Blueprint("booking_bp", __name__)

# ============================================================
#   GET /booking (list all)
# ============================================================
@booking_bp.route("/booking", methods=["GET"])
def list_booking():
    rows = get_all_booking()
    return jsonify(rows), 200


# ============================================================
#   POST /booking (create)
# ============================================================
@booking_bp.route("/booking", methods=["POST"])
def create_booking():

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = [
        "booking_date",
        "booking_time",
        "user_id",
        "store_id",
        "services",
        "customer",
        "total_price",
        "total_minutes",
        "type_booking_id",
        "status_booking_id",
    ]

    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:

        booking_id = insert_booking(data)

        insert_booking_services(booking_id, data["services"])

        return jsonify({
            "message": "Booking created successfully",
            "booking_id": booking_id
        }), 201

    except Exception as e:

        print("BOOKING ERROR:", str(e))

        return jsonify({
            "error": str(e)
        }), 400

# ============================================================
#   GET /booking/<id>
# ============================================================
@booking_bp.route("/booking/<int:bid>", methods=["GET"])
def get_booking(bid: int):
    row = get_booking_by_id(bid)
    if not row:
        return jsonify({"error": "Booking not found"}), 404
    return jsonify(row), 200


# ============================================================
#   PUT /booking/<id>
# ============================================================
@booking_bp.route("/booking/<int:bid>", methods=["PUT"])
def update_booking_route(bid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_booking(bid, data)

    if not updated:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify({
        "message": "Booking updated successfully",
        "booking_id": bid
    }), 200


# ============================================================
#   DELETE /booking/<id>
# ============================================================
@booking_bp.route("/booking/<int:bid>", methods=["DELETE"])
def delete_booking_route(bid: int):
    deleted = delete_booking(bid)

    if not deleted:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify({"message": "Booking deleted"}), 200


# ============================================================
#   GET /booking/<id>/detail
# ============================================================
@booking_bp.route("/booking/<int:bid>/detail", methods=["GET"])
def get_booking_detail(bid: int):
    rows = get_booking_with_services(bid)

    if not rows:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify(rows), 200




# ============================================================
#   GET /booking/user/<user_id> (ดึงการจองของผู้ใช้โดยระบุ user_id)
# ============================================================
@booking_bp.route("/booking/user/<int:user_id>", methods=["GET"])
def list_user_bookings(user_id: int):
    rows = get_user_bookings(user_id)
    return jsonify(rows), 200



# ============================================================
#   GET /booking/store/<store_id>
# ============================================================
@booking_bp.route("/booking/store/<int:store_id>", methods=["GET"])
def list_store_bookings(store_id: int):
    rows = get_store_bookings(store_id)
    return jsonify(rows), 200


@booking_bp.route("/bookings/<int:id>/status", methods=["PUT"])
def update_booking_status(id):
    data = request.get_json(silent=True)

    if not data or "status_booking_id" not in data:
        return jsonify({"error": "Missing status_booking_id"}), 400

    updated = update_booking_status_service(id, data["status_booking_id"])

    if not updated:
        return jsonify({"error": "Booking not found"}), 404

    return jsonify({"message": "Status updated successfully"}), 200


@booking_bp.route("/booking/alerts/<int:store_id>", methods=["GET"])
def alerts_route(store_id: int):
    rows = get_recent_alerts_by_store(store_id)
    return jsonify(rows), 200


# ============================================================
#   GET /schedule/<store_id>/<date>
# ============================================================
@booking_bp.route("/schedule/<int:store_id>/<date>", methods=["GET"])
def get_schedule_route(store_id, date):
    rows = get_schedule_from_bookings(store_id, date)
    return jsonify(rows), 200




@booking_bp.route("/booking/<int:booking_id>/assign", methods=["PUT"])
def assign_employee(booking_id):
    data = request.get_json()

    employee_id = data.get("employee_id")

    if not employee_id:
        return jsonify({"error": "employee_id required"}), 400

    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE bookings
        SET employee_id = %s
        WHERE booking_id = %s
    """

    cur.execute(sql, (employee_id, booking_id))
    conn.commit()

    cur.close()
    conn.close()

    return jsonify({"message": "Employee assigned"}), 200



# ============================================================
#   GET /booking/employee/<employee_id>/<date>
# ============================================================
@booking_bp.route("/booking/employee/<int:employee_id>/<date>", methods=["GET"])
def get_employee_schedule(employee_id, date):

    rows = get_employee_booked_times(employee_id, date)

    return jsonify(rows), 200

