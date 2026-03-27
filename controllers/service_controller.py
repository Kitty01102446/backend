from flask import Blueprint, request, jsonify
from services.service_service import (
    get_all_service,
    get_service_by_id,
    insert_service,
    update_service,
    delete_service,
    get_services_by_store,
    get_top_services_by_store,
    get_monthly_income_by_store,
    get_monthly_income_by_store_year
)

service_bp = Blueprint("service_bp", __name__)

# ============================================================
#   GET /service (list all) + POST /service (create)
# ============================================================
@service_bp.route("/service", methods=["GET"])
def list_service():
    rows = get_all_service()
    return jsonify(rows), 200


@service_bp.route("/service", methods=["POST"])
def create_service():
    """เพิ่ม service ใหม่ลงฐานข้อมูล"""

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["service_name", "price", "duration_minutes"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    service_name = data["service_name"]
    price = data["price"]
    duration = data["duration_minutes"]
    description = data.get("description", "")
    type_id = data.get("type_id", None)
    store_id = data.get("store_id", None)

    new_id = insert_service(service_name, price, duration, description, type_id, store_id)

    return jsonify({
        "message": "Service created successfully",
        "service_id": new_id
    }), 201


# ============================================================
# GET /service/<id> | PUT /service/<id> | DELETE /service/<id>
# ============================================================
@service_bp.route("/service/<int:sid>", methods=["GET"])
def get_service(sid: int):
    row = get_service_by_id(sid)
    if not row:
        return jsonify({"error": "Service not found"}), 404
    return jsonify(row), 200


@service_bp.route("/service/<int:sid>", methods=["PUT"])
def update_service_route(sid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_service(sid, data)

    if not updated:
        return jsonify({"error": "Service not found"}), 404

    return jsonify({
        "message": "Service updated successfully",
        "service_id": sid
    }), 200


@service_bp.route("/service/<int:sid>", methods=["DELETE"])
def delete_service_route(sid: int):
    deleted = delete_service(sid)

    if not deleted:
        return jsonify({"error": "Service not found"}), 404

    return jsonify({"message": "Service deleted"}), 200

# ============================================================
#   GET SERVICE BY STORE
# ============================================================
@service_bp.route("/service/store/<int:store_id>", methods=["GET"])
def get_services_by_store_route(store_id: int):
    rows = get_services_by_store(store_id)
    return jsonify(rows), 200


# ============================================================
#   GET TOP SERVICES BY STORE
# ============================================================
@service_bp.route("/report/top-services/<int:store_id>", methods=["GET"])
def top_services_route(store_id: int):
    rows = get_top_services_by_store(store_id)
    return jsonify(rows), 200


# ============================================================
#   GET MONTHLY INCOME
# ============================================================
@service_bp.route("/report/monthly-income/<int:store_id>", methods=["GET"])
def monthly_income_route(store_id: int):
    rows = get_monthly_income_by_store(store_id)
    return jsonify(rows), 200


@service_bp.route("/report/monthly-income/<int:store_id>/<int:year>", methods=["GET"])
def monthly_income_year_route(store_id: int, year: int):
    rows = get_monthly_income_by_store_year(store_id, year)
    return jsonify(rows), 200



@service_bp.route("/open-test")
def open_test():
    return {"msg": "open"}
