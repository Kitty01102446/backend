from flask import Blueprint, request, jsonify
from services.store_service import (
    get_all_store,
    get_store_by_id,
    insert_store,
    update_store,
    delete_store,
)
from services.db import get_conn


store_bp = Blueprint("store_bp", __name__)

# ============================================================
#   GET /store (list all) + POST /store (create)
# ============================================================
@store_bp.route("/store", methods=["GET"])
def list_store():
    rows = get_all_store()
    return jsonify(rows), 200


@store_bp.route("/store", methods=["POST"])
def create_store():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["store_name", "phone", "email", "address", "status_store_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    new_id = insert_store(
        store_name=data["store_name"],
        phone=data["phone"],
        email=data["email"],
        address=data["address"],
        image=data.get("image", ""),
        status_store_id=data["status_store_id"]
    )

    return jsonify({
        "message": "Store created successfully",
        "store_id": new_id
    }), 201


# ============================================================
#   GET /store/<id>  |  PUT /store/<id>  | DELETE /store/<id>
# ============================================================
@store_bp.route("/store/<int:sid>", methods=["GET"])
def get_store(sid: int):
    row = get_store_by_id(sid)
    if not row:
        return jsonify({"error": "Store not found"}), 404
    return jsonify(row), 200


@store_bp.route("/store/<int:sid>", methods=["PUT"])
def update_store_route(sid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_store(sid, data)

    if not updated:
        return jsonify({"error": "Store not found"}), 404

    return jsonify({
        "message": "Store updated successfully",
        "store_id": sid
    }), 200


@store_bp.route("/store/<int:sid>", methods=["DELETE"])
def delete_store_route(sid: int):
    deleted = delete_store(sid)

    if not deleted:
        return jsonify({"error": "Store not found"}), 404

    return jsonify({"message": "Store deleted"}), 200


# ============================================================
#   GET /store/by-user/<user_id>
# ============================================================
@store_bp.route("/store/by-user/<int:user_id>", methods=["GET"])
def get_store_by_user(user_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM store
        WHERE user_id = %s
        LIMIT 1
    """, (user_id,))

    store = cur.fetchone()

    cur.close()
    conn.close()

    if store:
        return jsonify({
            "has_store": True,
            "store": store
        }), 200
    else:
        return jsonify({
            "has_store": False
        }), 200


@store_bp.route("/store/<int:sid>/info", methods=["GET"])
def get_store_info(sid):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            store_id,
            store_name,
            phone,
            email,
            address,
            image
        FROM store
        WHERE store_id = %s
          AND deleted_at IS NULL
    """, (sid,))

    row = cur.fetchone()

    cur.close()
    conn.close()

    if not row:
        return jsonify({"error": "Store not found"}), 404

    return jsonify(row), 200







