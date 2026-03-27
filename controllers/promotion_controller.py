from flask import Blueprint, request, jsonify
from services.promotion_service import (
    get_all_promotion,
    get_promotion_by_id,
    insert_promotion,
    update_promotion,
    delete_promotion,
)

promotion_bp = Blueprint("promotion_bp", __name__)

# ============================================================
#   GET /promotion (list all) + POST /promotion (create)
# ============================================================
@promotion_bp.route("/promotion", methods=["GET"])
def list_promotion():
    rows = get_all_promotion()
    return jsonify(rows), 200


@promotion_bp.route("/promotion", methods=["POST"])
def create_promotion():
    """เพิ่ม promotion ใหม่ลงฐานข้อมูล"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["name", "discount", "store_id", "type_promo_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    name = data["name"]
    discount = data["discount"]
    store_id = data["store_id"]
    type_promo_id = data["type_promo_id"]

    new_id = insert_promotion(name, discount, store_id, type_promo_id)

    return jsonify({
        "message": "Promotion created successfully",
        "promotion_id": new_id
    }), 201


# ============================================================
#             GET /promotion/<id>
#             PUT /promotion/<id>
#           DELETE /promotion/<id>
# ============================================================
@promotion_bp.route("/promotion/<int:pid>", methods=["GET"])
def get_promotion(pid: int):
    row = get_promotion_by_id(pid)
    if not row:
        return jsonify({"error": "Promotion not found"}), 404
    return jsonify(row), 200


@promotion_bp.route("/promotion/<int:pid>", methods=["PUT"])
def update_promotion_route(pid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_promotion(pid, data)

    if not updated:
        return jsonify({"error": "Promotion not found"}), 404

    return jsonify({
        "message": "Promotion updated successfully",
        "promotion_id": pid
    }), 200


@promotion_bp.route("/promotion/<int:pid>", methods=["DELETE"])
def delete_promotion_route(pid: int):
    deleted = delete_promotion(pid)

    if not deleted:
        return jsonify({"error": "Promotion not found"}), 404

    return jsonify({"message": "Promotion deleted"}), 200
