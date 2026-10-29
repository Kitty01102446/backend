"""
Auth token (login) และตัวช่วยตรวจสอบสิทธิ์ Admin (เจ้าของร้าน) vs ช่าง (Staff)

Token เป็น itsdangerous signed token (เซ็นด้วย SECRET_KEY, มีวันหมดอายุ, ปลอมแปลง
ไม่ได้ถ้าไม่รู้ SECRET_KEY) เก็บแค่ {user_id, role_id} ส่วนสิทธิ์จริง (employee_id /
ร้านที่เป็นเจ้าของ) จะ query ฐานข้อมูลใหม่ทุกครั้งที่มี request เข้ามา เพื่อให้การ
เปลี่ยน role หรือผูกบัญชีมีผลทันที ไม่ต้องรอ token หมดอายุ
"""

import os
from functools import wraps

from flask import request, jsonify, g
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired

from services.employee_service import get_employee_by_user_id, get_employee_by_id
from services.store_service import get_store_ids_owned_by_user
from services.users_service import is_user_banned

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    SECRET_KEY = "dev-insecure-secret-change-me"
    print("⚠️  SECRET_KEY ไม่ถูกตั้งค่าใน environment -- ใช้ค่า dev เริ่มต้นที่ไม่ปลอดภัย "
          "กรุณาตั้ง SECRET_KEY ใน .env ก่อนขึ้น production")

_TOKEN_SALT = "nailshop-auth"
_TOKEN_MAX_AGE = 60 * 60 * 24 * 7  # 7 วัน

_serializer = URLSafeTimedSerializer(SECRET_KEY)


def generate_token(user_id: int, role_id: int) -> str:
    return _serializer.dumps({"user_id": user_id, "role_id": role_id}, salt=_TOKEN_SALT)


def decode_token(token: str):
    try:
        return _serializer.loads(token, salt=_TOKEN_SALT, max_age=_TOKEN_MAX_AGE)
    except (BadSignature, SignatureExpired):
        return None


def get_current_user():
    """คืน dict ของผู้ใช้ปัจจุบัน (query DB สดทุกครั้ง) หรือ None ถ้าไม่ได้ login/token ไม่ถูกต้อง"""
    auth_header = request.headers.get("Authorization", "")
    if not auth_header.startswith("Bearer "):
        return None

    payload = decode_token(auth_header[len("Bearer "):].strip())
    if not payload:
        return None

    user_id = payload.get("user_id")
    role_id = payload.get("role_id")
    if not user_id or not role_id:
        return None

    # แบนมีผลทันที แม้ token เดิมยังไม่หมดอายุ (ดูคอมเมนต์หัวไฟล์)
    if is_user_banned(user_id):
        return None

    current = {
        "user_id": user_id,
        "role_id": role_id,
        "employee_id": None,
        "employee_store_id": None,
        "owned_store_ids": [],
    }

    if role_id == 3:  # ช่าง (Staff)
        emp = get_employee_by_user_id(user_id)
        if emp:
            current["employee_id"] = emp["employee_id"]
            current["employee_store_id"] = emp["store_id"]
    elif role_id == 2:  # Admin ของร้าน (Shop Owner)
        current["owned_store_ids"] = get_store_ids_owned_by_user(user_id)
    # role_id == 4 (System Admin) ไม่ต้อง lookup เพิ่ม -- มีสิทธิ์ทุกร้าน/ทุกคนอยู่แล้ว
    # ผ่าน require_admin() ด้านล่าง ไม่ได้ผูกกับร้าน/พนักงานใดร้านหนึ่ง

    return current


def token_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        current = get_current_user()
        if not current:
            return jsonify({"error": "Unauthorized"}), 401
        g.current_user = current
        return f(*args, **kwargs)
    return wrapper


def require_admin():
    """คืน None ถ้าผ่าน (เป็นผู้ดูแลระบบ role_id=4) หรือ (response, status) ถ้าไม่ผ่าน"""
    current = getattr(g, "current_user", None)
    if not current:
        return jsonify({"error": "Unauthorized"}), 401
    if current["role_id"] != 4:
        return jsonify({"error": "Access denied: admin only"}), 403
    return None


def require_store_owner(store_id):
    """คืน None ถ้าผ่าน (เป็นเจ้าของร้านนี้จริง) หรือ (response, status) ถ้าไม่ผ่าน"""
    current = getattr(g, "current_user", None)
    if not current:
        return jsonify({"error": "Unauthorized"}), 401
    if int(store_id) not in current["owned_store_ids"]:
        return jsonify({"error": "Access denied: not the owner of this store"}), 403
    return None


def require_employee_access(employee_id, write=False):
    """คืน None ถ้าผ่าน หรือ (response, status) ถ้าไม่ผ่าน

    write=False (default): เจ้าของร้าน หรือ ช่างคนนั้นเอง (ดูข้อมูลตัวเอง)
    write=True: เฉพาะเจ้าของร้านของช่างคนนั้นเท่านั้น (แก้ไข/สั่งงานแทนช่าง)
    """
    current = getattr(g, "current_user", None)
    if not current:
        return jsonify({"error": "Unauthorized"}), 401

    emp = get_employee_by_id(employee_id)
    if not emp:
        return jsonify({"error": "Employee not found"}), 404

    if current["role_id"] == 2 and emp["store_id"] in current["owned_store_ids"]:
        return None

    if not write and current["role_id"] == 3 and current["employee_id"] == employee_id:
        return None

    return jsonify({"error": "Access denied"}), 403


def require_booking_store_owner(booking_id):
    from services.booking_service import get_booking_by_id

    current = getattr(g, "current_user", None)
    if not current:
        return jsonify({"error": "Unauthorized"}), 401

    booking = get_booking_by_id(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if booking["store_id"] not in current["owned_store_ids"]:
        return jsonify({"error": "Access denied"}), 403

    return None


def require_booking_customer_owner(booking_id):
    """คืน None ถ้าผ่าน (เป็นลูกค้าเจ้าของการจองนี้จริง) หรือ (response, status) ถ้าไม่ผ่าน"""
    from services.booking_service import get_booking_by_id

    current = getattr(g, "current_user", None)
    if not current:
        return jsonify({"error": "Unauthorized"}), 401

    booking = get_booking_by_id(booking_id)
    if not booking:
        return jsonify({"error": "Booking not found"}), 404

    if booking["user_id"] != current["user_id"]:
        return jsonify({"error": "Access denied: not the owner of this booking"}), 403

    return None


def require_self_user(user_id):
    """คืน None ถ้าผ่าน (ผู้ใช้กำลังเข้าถึงข้อมูลของตัวเอง) หรือ (response, status) ถ้าไม่ผ่าน"""
    current = getattr(g, "current_user", None)
    if not current:
        return jsonify({"error": "Unauthorized"}), 401

    if current["user_id"] != int(user_id):
        return jsonify({"error": "Access denied"}), 403

    return None
