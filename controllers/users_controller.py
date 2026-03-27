import os
import sys
from app import bcrypt
from flask import Blueprint, request, jsonify
from services.type_service_service import get_all_type_services
from werkzeug.security import generate_password_hash
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

GOOGLE_CLIENT_ID = "256511192038-aggr4jh4bmu9j5pmgo67v6mgccchj86l.apps.googleusercontent.com"



# บังคับหา Path ของโปรเจกต์
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

# ลอง Import จากจุดที่ใกล้ที่สุดก่อน
try:
    from services.db import get_conn
except ImportError:
    try:
        from config.db import get_conn
    except ImportError:
        # ถ้ายังไม่ได้อีก ให้ระบุ path ตรงๆ ไปที่ไฟล์
        import importlib.util
        spec = importlib.util.spec_from_file_location("db", os.path.join(BASE_DIR, "services/db.py"))
        db_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(db_mod)
        get_conn = db_mod.get_conn

from services.users_service import (
    get_all_users,
    get_user_by_id,
    insert_user,
    update_user,
    delete_user,
    login_user,
    login_google_service
)

users_bp = Blueprint('users', __name__, url_prefix='/users')

# ============================================================
#   POST /register (register a new user)
# ============================================================
@users_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()

    # ดึงค่าตาม Key ที่ React ส่งมาจริงๆ
    # ถ้า React ส่ง 'username' มา ก็ต้องดึง 'username'
    username = data.get('username') 
    nickname = data.get('nickname')
    phone = data.get('phone')
    email = data.get('email')
    password = data.get('password')
    role_id = data.get('role_id', 2)

    # เช็ค Debug ดูใน Terminal ว่าค่ามาไหม
    print(f"Received data: username={username}, nickname={nickname}")

    if not username or not email or not password:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    try:
        # ✅ 1. ทำการ Hash รหัสผ่านตรงนี้ก่อนส่งไป Service
        hashed_pw = generate_password_hash(password)
        
        # ✅ 2. เรียกใช้ Service โดยส่ง hashed_pw เข้าไป
        new_user_id = insert_user(
            username,
            nickname,
            phone,
            email,
            hashed_pw, # <--- ต้องเป็นตัวที่ hash แล้ว
            role_id
        )

        if new_user_id:
            return jsonify({
                'success': True,
                'message': 'User registered successfully',
                'user_id': new_user_id
            }), 201
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to insert user'
            }), 500

    except Exception as e:
        return jsonify({
            'success': False,
            'message': str(e)
        }), 400

# ============================================================
#   GET /users (list all)
# ============================================================
@users_bp.route("/users", methods=["GET"])
def list_users():
    rows = get_all_users()
    return jsonify(rows), 200


# ============================================================
#   POST /users (create)
# ============================================================
@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid or empty JSON payload"}), 400

    required = ["email", "username", "password"]
    for field in required:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    new_id = insert_user(
        username=data["username"],
        nickname=data.get("firstname", ""),
        phone=data.get("phone", ""),
        email=data["email"],
        password=data["password"],
        role_id=3,  # user
    )

    return jsonify({
        "message": "User created successfully",
        "user_id": new_id
    }), 201


# ============================================================
#   GET /users/<id>
# ============================================================
@users_bp.route("/users/<int:uid>", methods=["GET"])
def get_user(uid: int):
    row = get_user_by_id(uid)
    if not row:
        return jsonify({"error": "User not found"}), 404
    return jsonify(row), 200


# ============================================================
#   PUT /users/<id>
# ============================================================
@users_bp.route("/users/<int:uid>", methods=["PUT"])
def update_user_route(uid: int):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON"}), 400

    updated = update_user(uid, data)

    if not updated:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "message": "User updated successfully",
        "user_id": uid
    }), 200


# ============================================================
#   DELETE /users/<id> (soft delete)
# ============================================================
@users_bp.route("/users/<int:uid>", methods=["DELETE"])
def delete_user_route(uid: int):
    deleted = delete_user(uid)

    if not deleted:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"message": "User deleted"}), 200




@users_bp.route("/login_google", methods=["POST"])
def login_google():
    data = request.get_json()

    token = data.get("credential")

    if not token:
        return jsonify({"message": "Missing token"}), 400

    try:
        user = login_google_service(token)

        return jsonify({
            "status": "success",
            "user": user
        }), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 401

    except Exception as e:
        print("Google login error:", e)
        return jsonify({"message": "Internal server error"}), 500



# ============================================================
#   POST /login  ✅ (แก้ตรงนี้)
# ============================================================
@users_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"message": "Invalid JSON format"}), 400

    # ดึงข้อมูล identifier (email/phone) และ password
    identifier = data.get("identifier")
    password = data.get("password")

    # ตรวจสอบว่ามีข้อมูลที่จำเป็นครบถ้วน
    if not identifier or not password:
        return jsonify({"message": "Missing required fields: identifier or password"}), 400

    try:
        # เรียกใช้ฟังก์ชัน login_user เพื่อตรวจสอบข้อมูลในฐานข้อมูล
        user = login_user(identifier, password)

        if not user:
            return jsonify({
                "message": "Invalid credentials: email/phone or password is incorrect"
            }), 401

        # ส่งข้อมูลผู้ใช้กลับไป (ไม่ควรส่งข้อมูลรหัสผ่าน)
        return jsonify({
            "status": "success",
            "user": {
                "user_id": user["user_id"],
                "username": user["username"],
                "nickname": user["nickname"],
                "email": user["email"],
                "role_id": user["role_id"]
            }
        }), 200

    except Exception as e:
        # จับข้อผิดพลาดที่อาจเกิดขึ้น (เช่น ฐานข้อมูลเชื่อมต่อไม่ได้)
        print(f"Error during login: {str(e)}")
        return jsonify({
            "message": "Internal server error, please try again later"
        }), 500
# ============================================================
#   Register Store Logic (วางไว้ก่อน Route)
# ============================================================
def register_store_service(user_id, store_data, address_data, tags, services):
    conn = get_conn()
    cur = conn.cursor()
    try:
        # ---------- 1) STORE ----------
        name = store_data.get("name") or store_data.get("store_name")
        price = store_data.get("price", 0)
        phone = store_data.get("phone", "")
        email = store_data.get("email", "")

        if not name:
            raise ValueError("missing store name")

        sql_store = """
            INSERT INTO store (store_name, price, phone, email, user_id, status_store_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """
        cur.execute(sql_store, (name, price, phone, email, user_id, 1))
        store_id = cur.lastrowid

        # ---------- 2) ADDRESS ----------
        province = address_data.get("province", "")
        district = address_data.get("district", "")
        subdistrict = address_data.get("subdistrict", "")
        postal_code = address_data.get("zip") or address_data.get("postal_code") or ""
        recommend_text = address_data.get("recommend_text") or address_data.get("recommend") or ""
        street = address_data.get("street", "")
        open_time = address_data.get("open_time") or "10:00"
        close_time = address_data.get("close_time") or "20:00"

        sql_addr = """
            INSERT INTO store_address (
                store_id, province, district, subdistrict, postal_code,
                recommend_text, street, open_time, close_time
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(sql_addr, (
            store_id, province, district, subdistrict, postal_code,
            recommend_text, street, open_time, close_time
        ))

        # ---------- 3) TAGS ----------
        for t_name in (tags or []):
            cur.execute(
                "INSERT INTO store_tag (store_id, tag) VALUES (%s, %s)",
                (store_id, t_name)
            )

        # ---------- 4) SERVICES ----------
        for s in (services or []):
            # รองรับทั้งรูปแบบเก่า/ใหม่จาก frontend
            service_name = s.get("service_name") or s.get("name") or "บริการทั่วไป"
            s_price = s.get("price", 0)
            duration = s.get("duration_minutes") or s.get("minutes") or 0
            desc = s.get("description") or s.get("desc") or ""
            type_id = s.get("type_id") or s.get("type_service_id") or 1

            sql_service = """
                INSERT INTO service (store_id, service_name, price, duration_minutes, description, type_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cur.execute(sql_service, (store_id, service_name, s_price, duration, desc, type_id))


        conn.commit()
        return store_id

    except Exception as e:
        conn.rollback()
        print("Error register_store_service:", repr(e))
        return None

    finally:
        cur.close()
        conn.close()

# ============================================================
#   Route /register-store
# ============================================================

@users_bp.route("/register-store", methods=["POST"])
def register_store_route():
    data = request.get_json() or {}

    user_id = data.get("user_id")

    # ✅ รองรับทั้ง nested (store:{}) และ flat (name, price, ...)
    store_info = data.get("store") or {
        "name": data.get("name"),
        "price": data.get("price"),
        "phone": data.get("phone"),
        "email": data.get("email"),
        "desc": data.get("desc"),
        "open_time": data.get("open_time"),
        "close_time": data.get("close_time"),
    }

    # ✅ รองรับทั้ง nested address:{} และ flat province/district/...
    address_info = data.get("address") or {
        "street": data.get("street"),
        "province": data.get("province"),
        "district": data.get("district"),
        "subdistrict": data.get("subdistrict"),
        # ✅ แปลงให้เป็น zip ด้วย เพื่อกัน service ที่ใช้ key zip
        "zip": data.get("zip") or data.get("postal_code"),
        "postal_code": data.get("postal_code") or data.get("zip"),
        "recommend_text": data.get("recommend_text"),
        "open_time": data.get("open_time"),
        "close_time": data.get("close_time"),
    }

    tags = data.get("tags", []) or []
    services = data.get("services", []) or []

    if not user_id or not store_info.get("name"):
        return jsonify({"success": False, "message": "ข้อมูลไม่ครบถ้วน: ต้องมี user_id และ store.name"}), 400

    try:
        new_store_id = register_store_service(user_id, store_info, address_info, tags, services)

        # ✅ log ช่วยเช็คว่า service คืนค่าอะไร
        print("DEBUG new_store_id:", new_store_id, type(new_store_id))

        # ✅ กันเคส None / "0" / 0
        if new_store_id is not None:
            return jsonify({"success": True, "store_id": int(new_store_id)}), 201

        return jsonify({"success": False, "message": "register_store_service() returned None"}), 500

    except Exception as e:
        print("register-store error:", repr(e))
        return jsonify({"success": False, "message": str(e)}), 500
    
    

@users_bp.route("/type-services", methods=["GET"])
def type_services_route():
    try:
        rows = get_all_type_services()
        return jsonify(rows), 200
    except Exception as e:
        print("type-services error:", repr(e))
        return jsonify({"success": False, "message": str(e)}), 500



