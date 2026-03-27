from flask import Blueprint, request, jsonify
from services.employee_service import (
    get_all_employees,
    get_employee_by_id,
    insert_employee,
    update_employee,
    delete_employee,
    get_employee_by_store_id,
    get_employees_by_store
)

employee_bp = Blueprint("employee_bp", __name__)

# ============================================================
#   GET /employees (list all) + POST /employees (create)
# ============================================================
@employee_bp.route("/employees", methods=["GET"])
def list_employees():
    rows = get_all_employees()
    return jsonify(rows), 200


@employee_bp.route("/employees", methods=["POST"])
def create_employee():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["fullname", "phone", "position", "store_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    fullname = data["fullname"]
    phone = data["phone"]
    email = data.get("email")   # ✅ เพิ่มบรรทัดนี้
    position = data["position"]
    store_id = data["store_id"]

    new_id = insert_employee(
        fullname=fullname,
        phone=phone,
        email=email,
        position=position,
        store_id=store_id,
    )

    return jsonify({
        "message": "Employee created successfully",
        "employee_id": new_id
    }), 201

# ============================================================
#                  GET /employees/<id>
#                  PUT /employees/<id>
#                DELETE /employees/<id>
# ============================================================
@employee_bp.route("/employees/<int:eid>", methods=["GET"])
def get_employee(eid: int):
    row = get_employee_by_id(eid)
    if not row:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify(row), 200


@employee_bp.route("/employees/<int:eid>", methods=["PUT"])
def update_employee_route(eid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_employee(eid, data)

    if not updated:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({
        "message": "Employee updated successfully",
        "employee_id": eid
    }), 200


@employee_bp.route("/employees/<int:eid>", methods=["DELETE"])
def delete_employee_route(eid: int):
    deleted = delete_employee(eid)

    if not deleted:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({"message": "Employee deleted"}), 200


# ============================================================
#   GET /employees/store/<store_id>   ✅
# ============================================================
@employee_bp.route("/employees/store/<int:store_id>", methods=["GET"])
def get_employee_by_store(store_id):
    rows = get_employee_by_store_id(store_id)
    return jsonify(rows), 200


