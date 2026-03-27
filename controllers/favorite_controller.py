from flask import Blueprint, request, jsonify
from services.favorite_service import (
    get_all_favorite,
    get_favorite_by_id,
    insert_favorite,
    update_favorite,
    delete_favorite,
)

favorite_bp = Blueprint("favorite_bp", __name__)

# ============================================================
#   GET /favorite (list all) + POST /favorite (create)
# ============================================================
@favorite_bp.route("/favorite", methods=["GET"])
def list_favorite():
    rows = get_all_favorite()
    return jsonify(rows), 200


@favorite_bp.route("/favorite", methods=["POST"])
def create_favorite():
    """เพิ่ม favorite ใหม่ลงฐานข้อมูล"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    # ฟิลด์ที่ต้องมี เช่น store_id, user_id
    required = ["user_id", "store_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    # ดึงข้อมูลจาก body
    user_id = data["user_id"]
    store_id = data["store_id"]

    # Insert
    new_id = insert_favorite(
        user_id=user_id,
        store_id=store_id,
    )

    return jsonify({
        "message": "Favorite created successfully",
        "favorite_id": new_id
    }), 201


# ============================================================
#                  GET /favorite/<id>
#                  PUT /favorite/<id>
#                DELETE /favorite/<id>
# ============================================================
@favorite_bp.route("/favorite/<int:fid>", methods=["GET"])
def get_favorite(fid: int):
    row = get_favorite_by_id(fid)
    if not row:
        return jsonify({"error": "Favorite not found"}), 404
    return jsonify(row), 200


@favorite_bp.route("/favorite/<int:fid>", methods=["PUT"])
def update_favorite_route(fid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_favorite(fid, data)

    if not updated:
        return jsonify({"error": "Favorite not found"}), 404

    return jsonify({
        "message": "Favorite updated successfully",
        "favorite_id": fid
    }), 200


@favorite_bp.route("/favorite/<int:fid>", methods=["DELETE"])
def delete_favorite_route(fid: int):
    deleted = delete_favorite(fid)

    if not deleted:
        return jsonify({"error": "Favorite not found"}), 404

    return jsonify({"message": "Favorite deleted"}), 200
