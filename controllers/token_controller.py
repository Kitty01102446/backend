from flask import Blueprint, request, jsonify
from services.token_service import (
    get_all_tokens,
    get_token_by_id,
    insert_token,
    update_token,
    delete_token,
)

token_bp = Blueprint("token_bp", __name__)

# ============================================================
#   GET /token  +  POST /token
# ============================================================
@token_bp.route("/token", methods=["GET"])
def list_tokens():
    rows = get_all_tokens()
    return jsonify(rows), 200


@token_bp.route("/token", methods=["POST"])
def create_token():
    """สร้าง token ใหม่"""

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["jwt_key", "user_id", "expired_at"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    jwt_key = data["jwt_key"]
    user_id = data["user_id"]
    expired_at = data["expired_at"]

    new_id = insert_token(
        jwt_key=jwt_key,
        user_id=user_id,
        expired_at=expired_at
    )

    return jsonify({
        "message": "Token created successfully",
        "token_id": new_id
    }), 201


# ============================================================
#   GET /token/<id>
#   PUT /token/<id>
#   DELETE /token/<id>
# ============================================================
@token_bp.route("/token/<int:tid>", methods=["GET"])
def get_token(tid: int):
    row = get_token_by_id(tid)
    if not row:
        return jsonify({"error": "Token not found"}), 404
    return jsonify(row), 200


@token_bp.route("/token/<int:tid>", methods=["PUT"])
def update_token_route(tid: int):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_token(tid, data)
    if not updated:
        return jsonify({"error": "Token not found"}), 404

    return jsonify({
        "message": "Token updated successfully",
        "token_id": tid
    }), 200


@token_bp.route("/token/<int:tid>", methods=["DELETE"])
def delete_token_route(tid: int):
    deleted = delete_token(tid)
    if not deleted:
        return jsonify({"error": "Token not found"}), 404

    return jsonify({"message": "Token deleted"}), 200
