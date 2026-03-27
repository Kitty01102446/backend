from flask import Blueprint, request, jsonify
from services.payment_service import (
    get_all_payment,
    get_payment_by_id,
    insert_payment,
    update_payment,
    delete_payment,
)

payment_bp = Blueprint("payment", __name__, url_prefix="/payment")

# ============================================================
#   GET /payment (list all) + POST /payment (create)
# ============================================================
@payment_bp.route("/payment", methods=["GET"])
def list_payment():
    rows = get_all_payment()
    return jsonify(rows), 200


@payment_bp.route("/payment", methods=["POST"])
def create_payment():
    """เพิ่ม payment ใหม่ลงฐานข้อมูล"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    # ฟิลด์ที่ต้องมี เช่น method, payment_date, amount, booking_id, bill_id
    required = ["method", "payment_date", "amount", "booking_id", "bill_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # ดึงข้อมูลจาก body
    method = data["method"]
    payment_date = data["payment_date"]
    amount = data["amount"]
    booking_id = data["booking_id"]
    bill_id = data["bill_id"]

    # Insert
    new_id = insert_payment(
        method=method,
        payment_date=payment_date,
        amount=amount,
        booking_id=booking_id,
        bill_id=bill_id,
    )

    return jsonify({
        "message": "Payment created successfully",
        "payment_id": new_id
    }), 201


# ============================================================
#                  GET /payment/<id>
#                  PUT /payment/<id>
#                DELETE /payment/<id>
# ============================================================
@payment_bp.route("/payment/<int:pid>", methods=["GET"])
def get_payment(pid: int):
    row = get_payment_by_id(pid)
    if not row:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify(row), 200


@payment_bp.route("/payment/<int:pid>", methods=["PUT"])
def update_payment_route(pid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_payment(pid, data)

    if not updated:
        return jsonify({"error": "Payment not found"}), 404

    return jsonify({
        "message": "Payment updated successfully",
        "payment_id": pid
    }), 200


@payment_bp.route("/payment/<int:pid>", methods=["DELETE"])
def delete_payment_route(pid: int):
    deleted = delete_payment(pid)

    if not deleted:
        return jsonify({"error": "Payment not found"}), 404

    return jsonify({"message": "Payment deleted"}), 200
