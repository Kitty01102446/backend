from flask import Blueprint, request, jsonify
from services.type_promo_service import (
    get_all_type_promos,
    get_type_promo_by_id,
    insert_type_promo,
    update_type_promo,
    delete_type_promo,
)

type_promo_bp = Blueprint("type_promo_bp", __name__)

# ============================================================
#   GET /type_promo  +  POST /type_promo
# ============================================================
@type_promo_bp.route("/type_promo", methods=["GET"])
def list_type_promos():
    rows = get_all_type_promos()
    return jsonify(rows), 200


@type_promo_bp.route("/type_promo", methods=["POST"])
def create_type_promo():
    """เพิ่มข้อมูลประเภทโปรโมชั่น"""

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["name", "description"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    name = data["name"]
    description = data["description"]

    new_id = insert_type_promo(
        name=name,
        description=description
    )

    return jsonify({
        "message": "Type Promo created successfully",
        "type_promo_id": new_id
    }), 201


# ============================================================
#   GET /type_promo/<id>
#   PUT /type_promo/<id>
#   DELETE /type_promo/<id>
# ============================================================
@type_promo_bp.route("/type_promo/<int:tid>", methods=["GET"])
def get_type_promo(tid: int):
    row = get_type_promo_by_id(tid)
    if not row:
        return jsonify({"error": "Type Promo not found"}), 404
    return jsonify(row), 200


@type_promo_bp.route("/type_promo/<int:tid>", methods=["PUT"])
def update_type_promo_route(tid: int):
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_type_promo(tid, data)
    if not updated:
        return jsonify({"error": "Type Promo not found"}), 404

    return jsonify({
        "message": "Type Promo updated successfully",
        "type_promo_id": tid
    }), 200


@type_promo_bp.route("/type_promo/<int:tid>", methods=["DELETE"])
def delete_type_promo_route(tid: int):
    deleted = delete_type_promo(tid)
    if not deleted:
        return jsonify({"error": "Type Promo not found"}), 404

    return jsonify({"message": "Type Promo deleted"}), 200
