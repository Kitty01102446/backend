from flask import Blueprint, request, jsonify
from services.bill_service import (
    get_all_bill,
    get_bill_by_id,
    insert_bill,
    update_bill,
    delete_bill,
)

bill_bp = Blueprint("bill_bp", __name__)

# ============================================================
#   GET /bill (list all) + POST /bill (create)
# ============================================================
@bill_bp.route("/bill", methods=["GET"])
def list_bill():
    rows = get_all_bill()
    return jsonify(rows), 200


@bill_bp.route("/bill", methods=["POST"])
def create_bill():
    """เพิ่มบิลใหม่ลงฐานข้อมูล"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    # ตัวอย่างฟิลด์ที่ต้องมี (แก้ตามตาราง bill ของเธอ)
    required = ["total_amount", "store_id", "status_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # ดึงข้อมูล
    total_amount = data["total_amount"]
    store_id = data["store_id"]
    status_id = data["status_id"]

    # Insert
    new_id = insert_bill(
        total_amount=total_amount,
        store_id=store_id,
        status_id=status_id,
    )

    return jsonify({
        "message": "Bill created successfully",
        "bill_id": new_id
    }), 201


# ============================================================
#             GET /bill/<id>
#             PUT /bill/<id>
#           DELETE /bill/<id>
# ============================================================
@bill_bp.route("/bill/<int:bid>", methods=["GET"])
def get_bill(bid: int):
    row = get_bill_by_id(bid)
    if not row:
        return jsonify({"error": "Bill not found"}), 404
    return jsonify(row), 200


@bill_bp.route("/bill/<int:bid>", methods=["PUT"])
def update_bill_route(bid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_bill(bid, data)

    if not updated:
        return jsonify({"error": "Bill not found"}), 404

    return jsonify({
        "message": "Bill updated successfully",
        "bill_id": bid
    }), 200


@bill_bp.route("/bill/<int:bid>", methods=["DELETE"])
def delete_bill_route(bid: int):
    deleted = delete_bill(bid)

    if not deleted:
        return jsonify({"error": "Bill not found"}), 404

    return jsonify({"message": "Bill deleted"}), 200
