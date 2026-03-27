from flask import Blueprint, request, jsonify
from services.click_log_service import (
    get_all_click_logs,
    get_click_log_by_id,
    insert_click_log,
    update_click_log,
    delete_click_log,
)

click_log_bp = Blueprint("click_log", __name__, url_prefix="/click_log")

# ============================================================
#   GET /click_log   +   POST /click_log
# ============================================================
@click_log_bp.route("/click_log", methods=["GET"])
def list_click_logs():
    rows = get_all_click_logs()
    return jsonify(rows), 200


@click_log_bp.route("/click_log", methods=["POST"])
def create_click_log():
    """เพิ่ม log ใหม่เมื่อมีการคลิก"""

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["user_id", "store_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    user_id = data["user_id"]
    store_id = data["store_id"]

    new_id = insert_click_log(
        user_id=user_id,
        store_id=store_id
    )

    return jsonify({
        "message": "Click Log created successfully",
        "click_log_id": new_id
    }), 201


# ============================================================
#   GET /click_log/<id>
#   PUT /click_log/<id>
#   DELETE /click_log/<id>
# ============================================================
@click_log_bp.route("/click_log/<int:cid>", methods=["GET"])
def get_click_log(cid: int):
    row = get_click_log_by_id(cid)
    if not row:
        return jsonify({"error": "Click Log not found"}), 404
    return jsonify(row), 200


@click_log_bp.route("/click_log/<int:cid>", methods=["PUT"])
def update_click_log_route(cid: int):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_click_log(cid, data)
    if not updated:
        return jsonify({"error": "Click Log not found"}), 404

    return jsonify({
        "message": "Click Log updated successfully",
        "click_log_id": cid
    }), 200


@click_log_bp.route("/click_log/<int:cid>", methods=["DELETE"])
def delete_click_log_route(cid: int):
    deleted = delete_click_log(cid)
    if not deleted:
        return jsonify({"error": "Click Log not found"}), 404

    return jsonify({"message": "Click Log deleted"}), 200
