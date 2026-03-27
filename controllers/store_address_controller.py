from flask import Blueprint, request, jsonify
from services.store_address_service import (
    get_all_store_address,
    get_store_address_by_id,
    insert_store_address,
    update_store_address,
    delete_store_address,
)

store_address_bp = Blueprint("store_address", __name__, url_prefix="/store_address")

# ============================================================
#   GET /store_address
# ============================================================
@store_address_bp.route("/store_address", methods=["GET"])
def list_store_address():
    rows = get_all_store_address()
    return jsonify({
        "status": "success",
        "data": rows
    }), 200


# ============================================================
#   POST /store_address
# ============================================================
@store_address_bp.route("/store_address", methods=["POST"])
def create_store_address():
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    # required ขั้นต่ำ
    required = ["province", "district", "subdistrict", "postal_code", "store_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    new_id = insert_store_address(data)

    return jsonify({
        "status": "success",
        "message": "Store address created successfully",
        "store_address_id": new_id
    }), 201


# ============================================================
#   GET /store_address/<id>
# ============================================================
@store_address_bp.route("/store_address/<int:sid>", methods=["GET"])
def get_store_address(sid: int):
    row = get_store_address_by_id(sid)
    if not row:
        return jsonify({"error": "Store address not found"}), 404

    return jsonify({
        "status": "success",
        "data": row
    }), 200


# ============================================================
#   PUT /store_address/<id>
# ============================================================
@store_address_bp.route("/store_address/<int:sid>", methods=["PUT"])
def update_store_address_route(sid: int):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    updated = update_store_address(sid, data)
    if not updated:
        return jsonify({"error": "Store address not found"}), 404

    return jsonify({
        "status": "success",
        "message": "Store address updated successfully",
        "store_address_id": sid
    }), 200


# ============================================================
#   DELETE /store_address/<id>  (Soft delete)
# ============================================================
@store_address_bp.route("/store_address/<int:sid>", methods=["DELETE"])
def delete_store_address_route(sid: int):
    deleted = delete_store_address(sid)
    if not deleted:
        return jsonify({"error": "Store address not found"}), 404

    return jsonify({
        "status": "success",
        "message": "Store address deleted"
    }), 200
