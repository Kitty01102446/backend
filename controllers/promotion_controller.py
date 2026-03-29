from flask import Blueprint, request, jsonify
from services.promotion_service import (
    get_all_promotion,
    get_promotion_by_id,
    insert_promotion,
    update_promotion,
    delete_promotion,
    get_promotion_by_store,
    
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

    # ✅ เพิ่ม detail เข้าไปใน required
    required = ["name", "detail", "discount", "store_id", "type_promo_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # ✅ ดึงค่าจาก request
    name = data["name"]
    detail = data["detail"]   # 🔥 เพิ่มตรงนี้
    discount = data["discount"]
    store_id = data["store_id"]
    type_promo_id = data["type_promo_id"]
    promo_code = data.get("promo_code")

    # optional
    start_date = data.get("start_date")
    end_date = data.get("end_date")

    # ✅ เรียก service (ต้องแก้ service ด้วยนะ)
    new_id = insert_promotion(
        name,
        detail,
        discount,
        store_id,
        type_promo_id,
        start_date,
        end_date,
        promo_code
    )

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


@promotion_bp.route("/promotion/store/<int:store_id>", methods=["GET"])
def get_promotion_by_store_route(store_id):
    rows = get_promotion_by_store(store_id)
    return jsonify(rows), 200
