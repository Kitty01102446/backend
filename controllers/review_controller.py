from flask import Blueprint, request, jsonify
from services.review_service import (
    get_all_review,
    get_review_by_id,
    get_reviews_by_store,
    insert_review,
    update_review,
    delete_review,
)

review_bp = Blueprint("review_bp", __name__)

# ============================================================
#   GET /review (list all) + POST /review (create)
# ============================================================
@review_bp.route("/review", methods=["GET"])
def list_review():
    rows = get_all_review()
    return jsonify(rows), 200


@review_bp.route("/review/store/<int:store_id>", methods=["GET"])
def list_review_by_store(store_id: int):
    rows = get_reviews_by_store(store_id)
    return jsonify(rows), 200


@review_bp.route("/review", methods=["POST"])
def create_review():
    """เพิ่ม review ใหม่ลงฐานข้อมูล"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["rating", "comment", "user_id", "store_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    rating = data["rating"]
    comment = data["comment"]
    user_id = data["user_id"]
    store_id = data["store_id"]

    new_id = insert_review(rating, comment, user_id, store_id)

    return jsonify({
        "message": "Review created successfully",
        "review_id": new_id
    }), 201


# ============================================================
# GET /review/<id>  |  PUT /review/<id>  |  DELETE /review/<id>
# ============================================================
@review_bp.route("/review/<int:rid>", methods=["GET"])
def get_review(rid: int):
    row = get_review_by_id(rid)
    if not row:
        return jsonify({"error": "Review not found"}), 404
    return jsonify(row), 200


@review_bp.route("/review/<int:rid>", methods=["PUT"])
def update_review_route(rid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_review(rid, data)

    if not updated:
        return jsonify({"error": "Review not found"}), 404

    return jsonify({
        "message": "Review updated successfully",
        "review_id": rid
    }), 200


@review_bp.route("/review/<int:rid>", methods=["DELETE"])
def delete_review_route(rid: int):
    deleted = delete_review(rid)

    if not deleted:
        return jsonify({"error": "Review not found"}), 404

    return jsonify({"message": "Review deleted"}), 200
