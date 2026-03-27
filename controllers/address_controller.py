from flask import Blueprint, request, jsonify
from services.address_service import (
    get_all_address,
    get_address_by_id,
    insert_address,
    update_address,
    delete_address,
)

address_bp = Blueprint("address", __name__, url_prefix="/address")

# ============================================================
#   GET /address (list all) + POST /address (create)
# ============================================================
@address_bp.route("/address", methods=["GET"])
def list_address():
    rows = get_all_address()
    return jsonify(rows), 200


@address_bp.route("/address", methods=["POST"])
def create_address():
    """เพิ่มที่อยู่ใหม่ลงฐานข้อมูล"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    # ตัวอย่างฟิลด์ที่ต้องมี (แก้ตามตาราง address ของเธอ)
    required = ["province", "district", "subdistrict", "postal_code", "user_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # ดึงข้อมูล
    province = data["province"]
    district = data["district"]
    subdistrict = data["subdistrict"]
    postal_code = data["postal_code"]
    user_id = data["user_id"]

    # Insert
    new_id = insert_address(
        province=province,
        district=district,
        subdistrict=subdistrict,
        postal_code=postal_code,
        user_id=user_id,
    )

    return jsonify({
        "message": "Address created successfully",
        "address_id": new_id
    }), 201


# ============================================================
#             GET /address/<id>
#             PUT /address/<id>
#           DELETE /address/<id>
# ============================================================
@address_bp.route("/address/<int:aid>", methods=["GET"])
def get_address(aid: int):
    row = get_address_by_id(aid)
    if not row:
        return jsonify({"error": "Address not found"}), 404
    return jsonify(row), 200


@address_bp.route("/address/<int:aid>", methods=["PUT"])
def update_address_route(aid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_address(aid, data)

    if not updated:
        return jsonify({"error": "Address not found"}), 404

    return jsonify({
        "message": "Address updated successfully",
        "address_id": aid
    }), 200


@address_bp.route("/address/<int:aid>", methods=["DELETE"])
def delete_address_route(aid: int):
    deleted = delete_address(aid)

    if not deleted:
        return jsonify({"error": "Address not found"}), 404

    return jsonify({"message": "Address deleted"}), 200
