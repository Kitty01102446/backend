from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from services.employee_service import (
    get_all_employees,
    get_employee_by_id,
    insert_employee,
    update_employee,
    delete_employee,
    get_employee_by_store_id,
    get_public_employees_by_store,
    get_employees_by_store,
    set_employee_user_id,
)
from services.users_service import insert_user, get_user_by_contact, set_user_role
from services.auth_service import token_required, require_store_owner, require_employee_access

employee_bp = Blueprint("employee_bp", __name__)

# ============================================================
#   GET /employees (list all) + POST /employees (create)
# ============================================================
@employee_bp.route("/employees", methods=["GET"])
def list_employees():
    rows = get_all_employees()
    return jsonify(rows), 200


@employee_bp.route("/employees", methods=["POST"])
@token_required
def create_employee():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["fullname", "phone", "position", "store_id"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    guard = require_store_owner(data["store_id"])
    if guard:
        return guard

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
@token_required
def get_employee(eid: int):
    guard = require_employee_access(eid, write=False)
    if guard:
        return guard

    row = get_employee_by_id(eid)
    if not row:
        return jsonify({"error": "Employee not found"}), 404
    return jsonify(row), 200


@employee_bp.route("/employees/<int:eid>", methods=["PUT"])
@token_required
def update_employee_route(eid: int):
    guard = require_employee_access(eid, write=True)
    if guard:
        return guard

    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    if data.get("store_id"):
        guard = require_store_owner(data["store_id"])
        if guard:
            return guard

    updated = update_employee(eid, data)

    if not updated:
        return jsonify({"error": "Employee not found"}), 404

    return jsonify({
        "message": "Employee updated successfully",
        "employee_id": eid
    }), 200


@employee_bp.route("/employees/<int:eid>", methods=["DELETE"])
@token_required
def delete_employee_route(eid: int):
    guard = require_employee_access(eid, write=True)
    if guard:
        return guard

    emp = get_employee_by_id(eid)
    deleted = delete_employee(eid)

    if not deleted:
        return jsonify({"error": "Employee not found"}), 404

    # ถ้าพนักงานคนนี้มีบัญชี login ผูกอยู่ ให้คืน role เป็น user ธรรมดา เพราะ
    # ไม่ใช่ช่างของร้านนี้แล้ว (ตอนนี้เขาสมัครเปิดร้านเองได้)
    if emp and emp.get("user_id"):
        set_user_role(emp["user_id"], 1)

    return jsonify({"message": "Employee deleted"}), 200


# ============================================================
#   GET /employees/store/<store_id>   ✅
# ============================================================
@employee_bp.route("/employees/store/<int:store_id>", methods=["GET"])
@token_required
def get_employee_by_store(store_id):
    guard = require_store_owner(store_id)
    if guard:
        return guard

    rows = get_employee_by_store_id(store_id)
    return jsonify(rows), 200


# ============================================================
#   GET /employees/store/<store_id>/public  (ไม่ต้อง login)
#   ใช้กับหน้าจองของลูกค้า -- ให้เลือกช่างได้ คืนแค่ชื่อ/ตำแหน่ง ไม่มีข้อมูล
#   ที่อ่อนไหว (เบอร์โทร/อีเมล/เงินเดือน) เหมือน endpoint ด้านบนที่เจ้าของร้าน
#   ใช้จัดการพนักงาน
# ============================================================
@employee_bp.route("/employees/store/<int:store_id>/public", methods=["GET"])
def get_public_employee_list(store_id):
    rows = get_public_employees_by_store(store_id)
    return jsonify(rows), 200


# ============================================================
#   POST /employees/<id>/account  -- Admin สร้างบัญชี login ให้ช่างคนนี้
#   (ผูก employee.user_id เข้ากับ users แถวใหม่ role_id=3 "Staff")
# ============================================================
@employee_bp.route("/employees/<int:eid>/account", methods=["POST"])
@token_required
def create_employee_account(eid: int):
    guard = require_employee_access(eid, write=True)
    if guard:
        return guard

    emp = get_employee_by_id(eid)
    if emp.get("user_id"):
        return jsonify({"error": "Employee already has a login account"}), 409

    data = request.get_json(silent=True) or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    emp_email = emp.get("email")
    if emp_email:
        conflict = get_user_by_contact(email=emp_email)
        if conflict:
            return jsonify({
                "error": f"อีเมล {emp_email} ถูกใช้กับบัญชีอื่นอยู่แล้ว (username: {conflict['username']}) กรุณาแก้ไขอีเมลของพนักงานคนนี้ก่อนสร้างบัญชี"
            }), 409

    hashed_pw = generate_password_hash(password)
    new_user_id = insert_user(
        username=username,
        nickname=emp.get("fullname"),
        phone=emp.get("phone"),
        email=emp.get("email"),
        password=hashed_pw,
        role_id=3,  # Staff / ช่าง
    )

    if not new_user_id:
        return jsonify({"error": "Failed to create login account"}), 500

    set_employee_user_id(eid, new_user_id)

    return jsonify({
        "message": "Login account created",
        "user_id": new_user_id,
        "username": username,
    }), 201
