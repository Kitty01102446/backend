from services.db import get_conn
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import pymysql
import random
from datetime import datetime, timedelta
from google.oauth2 import id_token
from google.auth.transport import requests as grequests

# ============================================================
#                     SELECT ALL USERS
# ============================================================
def get_all_users():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE deleted_at IS NULL")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT USER BY ID
# ============================================================
def get_user_by_id(uid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            user_id,
            username,
            nickname,
            phone,
            email,
            role_id,
            created_at,
            updated_at,
            deleted_at
        FROM users
        WHERE user_id = %s
          AND deleted_at IS NULL
    """, (uid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT USER
# ============================================================
def insert_user(username, nickname, phone, email, password, role_id):
    conn = get_conn()
    cur = conn.cursor()
    
    # ตรวจสอบว่า %s เรียงลำดับตรงกับตัวแปรด้านล่าง
    sql = """
        INSERT INTO users (username, nickname, phone, email, password, role_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
    """
    
    try:
        cur.execute(sql, (username, nickname, phone, email, password, role_id))
        new_id = cur.lastrowid
        conn.commit()
        return new_id
    except Exception as e:
        print(f"Error inserting user: {e}")
        conn.rollback()  # ย้อนกลับการเปลี่ยนแปลงในกรณีเกิดข้อผิดพลาด
        return None
    finally:
        cur.close()
        conn.close()

# ============================================================
#                      UPDATE USER
# ============================================================
def update_user(uid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    fields = []
    values = []

    # อนุญาตให้แก้เฉพาะข้อมูลโปรไฟล์
    if "username" in data and data["username"]:
        fields.append("username=%s")
        values.append(data["username"])

    if "nickname" in data and data["nickname"]:
        fields.append("nickname=%s")
        values.append(data["nickname"])

    if "phone" in data and data["phone"]:
        fields.append("phone=%s")
        values.append(data["phone"])

    if "email" in data and data["email"]:
        fields.append("email=%s")
        values.append(data["email"])

    # ❌ ไม่แก้ password / role_id จากหน้านี้
    # ถ้าจะเปลี่ยน password → ควรทำ endpoint แยก

    if not fields:
        cur.close()
        conn.close()
        return False

    sql = f"""
        UPDATE users
        SET {', '.join(fields)},
            updated_at = NOW()
        WHERE user_id = %s
          AND deleted_at IS NULL
    """

    values.append(uid)

    cur.execute(sql, tuple(values))
    conn.commit()

    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated



# ============================================================
#                  DELETE USER (SOFT DELETE)
# ============================================================
def delete_user(uid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute(sql, (uid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted

# ============================================================
#                      LOGIN USER
# ============================================================
def login_user(identifier, password):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)  # ใช้ DictCursor เพื่อให้ผลลัพธ์เป็น Dictionary

    sql = """
        SELECT user_id, username, nickname, phone, email, role_id, password,
               is_banned, ban_reason
        FROM users
        WHERE (email = %s OR phone = %s)
          AND deleted_at IS NULL
        LIMIT 1
    """
    cur.execute(sql, (identifier, identifier))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if not user:
        return None  # หากไม่พบผู้ใช้

    stored_password = user['password']

    # ตรวจสอบว่า stored_password ใช้ hash method ที่รองรับ (เช่น bcrypt)
    if not stored_password or not check_password_hash(stored_password, password):
        return None  # รหัสผ่านไม่ตรงกัน

    # บัญชีถูกแบน -- เช็คหลังรหัสผ่านถูกต้องแล้วเท่านั้น (ไม่รั่วไหลว่าบัญชีไหนถูก
    # แบนให้คนที่เดารหัสผ่านผิดอยู่)
    if user.get("is_banned"):
        raise PermissionError(user.get("ban_reason") or "บัญชีนี้ถูกระงับการใช้งาน")

    # ✅ แนบข้อมูลสิทธิ์เพิ่มเติมตาม role -- ช่าง (role_id=3) แนบ employee_id/store_id
    # ของตัวเอง, เจ้าของร้าน (role_id=2) แนบรายชื่อร้านที่เป็นเจ้าของ
    from services.employee_service import get_employee_by_user_id
    from services.store_service import get_store_ids_owned_by_user

    user["employee_id"] = None
    user["employee_store_id"] = None
    user["owned_store_ids"] = []

    if user["role_id"] == 3:
        emp = get_employee_by_user_id(user["user_id"])
        if emp:
            user["employee_id"] = emp["employee_id"]
            user["employee_store_id"] = emp["store_id"]
    elif user["role_id"] == 2:
        user["owned_store_ids"] = get_store_ids_owned_by_user(user["user_id"])

    return user

# ============================================================
#                 register store user by id
# ============================================================


def register_store_service(user_id, store_data, address_data, tags, services):
    conn = get_conn()
    cur = conn.cursor()
    try:
        # 1. เพิ่มข้อมูลร้านค้า
        sql_store = "INSERT INTO store (store_name, store_description, user_id, status_store_id, created_at) VALUES (%s, %s, %s, %s, NOW())"
        cur.execute(sql_store, (store_data['name'], store_data.get('desc', ''), user_id, 1))
        store_id = cur.lastrowid

        # 2. เพิ่มที่อยู่ร้าน
        sql_addr = "INSERT INTO store_address (store_id, address_detail, province, city, zip_code) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(sql_addr, (store_id, address_data['detail'], address_data['province'], address_data.get('city', ''), address_data.get('zip', '')))

        # 3. เพิ่ม Tags (สมมติว่าส่งมาเป็นข้อความ ต้องจัดการตามโครงสร้างตารางคุณ)
        # ถ้าตาราง store_tag เก็บเป็นข้อความตรงๆ:
        for t_name in tags:
            cur.execute("INSERT INTO store_tag (store_id, tag_name) VALUES (%s, %s)", (store_id, t_name))

        # 4. เพิ่ม Services (แก้ไขการย่อหน้าและ Key ให้ตรงกับ React)
        for s in services:
            sql_service = """
                INSERT INTO store_service_list (store_id, service_name, price, duration_minutes)
                VALUES (%s, %s, %s, %s)
            """
            # ใช้ get() เพื่อป้องกัน Key Error ถ้า React ส่งชื่อ field มาไม่ตรง
            cur.execute(sql_service, (
                store_id, 
                s.get('service_name'), 
                s.get('price'), 
                s.get('duration_minutes')
            ))

        conn.commit()
        return store_id
    except Exception as e:
        conn.rollback()
        print(f"Python Error: {e}") # ดู Error นี้ใน Terminal ของคุณ
        return None
    finally:
        cur.close()
        conn.close()

def reset_password(user_id, new_password):
    conn = get_conn()
    cur = conn.cursor()

    # แฮชรหัสผ่านใหม่
    hashed_password = generate_password_hash(new_password)

    sql = """
        UPDATE users
        SET password = %s, updated_at = NOW()
        WHERE user_id = %s
    """
    try:
        cur.execute(sql, (hashed_password, user_id))
        conn.commit()
    except Exception as e:
        print(f"Error resetting password: {e}")
        conn.rollback()
    finally:
        cur.close()
        conn.close()


# ============================================================
#                 ลืมรหัสผ่าน (Forgot Password)
# ============================================================
RESET_CODE_TTL_MINUTES = 15


def get_user_by_contact(email=None, phone=None):
    """หา user จาก email หรือ phone (ใช้เช็คซ้ำก่อนสร้างบัญชีใหม่ เพราะคอลัมน์ email มี
    UNIQUE KEY -- ถ้าไม่เช็คก่อน insert_user จะ insert ไม่ผ่านแบบเงียบ ๆ แล้วคืน None
    ทำให้ผู้เรียกเห็นแค่ 500 ทั่วไปโดยไม่รู้สาเหตุ) คืน None ถ้าไม่พบ"""
    if not email and not phone:
        return None
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)
    cur.execute(
        "SELECT user_id, username, email FROM users WHERE deleted_at IS NULL AND (email=%s OR phone=%s) LIMIT 1",
        (email, phone)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def is_user_banned(user_id: int) -> bool:
    """เช็คสถานะแบนสด ๆ ทุก request (ดู auth_service.get_current_user) เพื่อให้การ
    แบนมีผลทันทีแม้ token เดิมยังไม่หมดอายุ"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT is_banned FROM users WHERE user_id=%s AND deleted_at IS NULL", (user_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return bool(row and row.get("is_banned"))


def set_user_role(user_id: int, role_id: int):
    """ใช้ตอนเจ้าของร้านลบพนักงานที่มีบัญชี login ผูกอยู่ -- คืน role เป็น user
    ธรรมดา (role_id=1) เพราะบัญชีนั้นไม่ใช่ช่างของร้านนี้แล้ว"""
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET role_id=%s, updated_at=NOW() WHERE user_id=%s",
        (role_id, user_id)
    )
    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated


def request_password_reset(identifier):
    """หา user จาก email/เบอร์โทร แล้วสร้างรหัสรีเซ็ต 6 หลัก เก็บไว้ในตาราง token เดิม
    (เว็บนี้ยังไม่มีระบบส่งอีเมลจริง -- ใช้โหมดพัฒนา แสดงรหัสให้ผู้ใช้บนหน้าจอโดยตรง)
    คืนค่า None ถ้าไม่พบผู้ใช้"""
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute(
        "SELECT user_id, username, email FROM users WHERE (email=%s OR phone=%s) AND deleted_at IS NULL LIMIT 1",
        (identifier, identifier)
    )
    user = cur.fetchone()
    if not user:
        cur.close()
        conn.close()
        return None

    reset_code = f"{random.randint(0, 999999):06d}"
    expires_at = datetime.now() + timedelta(minutes=RESET_CODE_TTL_MINUTES)

    cur.execute(
        "INSERT INTO token (jwt_key, user_id, created_at, expired_at) VALUES (%s, %s, NOW(), %s)",
        (reset_code, user["user_id"], expires_at)
    )
    conn.commit()
    cur.close()
    conn.close()

    return {
        "user_id": user["user_id"],
        "username": user["username"],
        "reset_code": reset_code,
        "expires_at": expires_at.isoformat(),
    }


def confirm_password_reset(reset_code, new_password):
    """ตรวจสอบรหัสรีเซ็ตกับตาราง token แล้วตั้งรหัสผ่านใหม่ (reuse reset_password())
    คืนค่า True/False"""
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute(
        "SELECT token_id, user_id, expired_at FROM token WHERE jwt_key=%s ORDER BY token_id DESC LIMIT 1",
        (reset_code,)
    )
    row = cur.fetchone()

    if not row or not row["expired_at"] or row["expired_at"] < datetime.now():
        cur.close()
        conn.close()
        return False

    cur.execute("DELETE FROM token WHERE token_id=%s", (row["token_id"],))
    conn.commit()
    cur.close()
    conn.close()

    reset_password(row["user_id"], new_password)
    return True


def register_user(username, nickname, phone, email, password, role_id):
    conn = get_conn()
    cur = conn.cursor()

    # แฮชรหัสผ่าน
    hashed_password = generate_password_hash(password)

    sql = """
        INSERT INTO users (username, nickname, phone, email, password, role_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())
    """

    try:
        cur.execute(sql, (username, nickname, phone, email, hashed_password, role_id))
        new_id = cur.lastrowid
        conn.commit()
        return new_id
    except Exception as e:
        print(f"Error inserting user: {e}")
        conn.rollback()
        return None
    finally:
        cur.close()
        conn.close()



GOOGLE_CLIENT_ID = "256511192038-aggr4jh4bmu9j5pmgo67v6mgccchj86l.apps.googleusercontent.com"


def login_google_service(token):
    try:
        # ✅ verify token
        idinfo = id_token.verify_oauth2_token(
            token,
            grequests.Request(),
            GOOGLE_CLIENT_ID
        )

        email = idinfo.get("email")
        name = idinfo.get("name")
        google_id = idinfo.get("sub")

        # 🔥 กันเคสไม่มี email
        if not email:
            email = f"google_{google_id}@noemail.com"

        conn = get_conn()
        cur = conn.cursor(pymysql.cursors.DictCursor)  # ✅ FIX ตรงนี้

        # ------------------------------
        # ✅ หา user
        # ------------------------------
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()

        # ------------------------------
        # 🔥 ถ้าไม่มี → สร้างใหม่
        # ------------------------------
        if not user:
            cur.execute("""
                INSERT INTO users (
                    username,
                    nickname,
                    email,
                    password,
                    role_id,
                    created_at
                )
                VALUES (%s, %s, %s, %s, %s, NOW())
            """, (
                name,
                name,
                email,
                None,
                1
            ))
            conn.commit()

            # ดึง user ใหม่
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()

        cur.close()
        conn.close()

        # ------------------------------
        # ✅ return user
        # ------------------------------
        return {
            "user_id": user["user_id"],
            "username": user["username"],
            "nickname": user["nickname"],
            "email": user["email"],
            "role_id": user["role_id"]
        }

    except Exception as e:
        print("Google login error:", e)
        raise Exception("Google login failed")






