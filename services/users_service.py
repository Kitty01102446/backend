from services.db import get_conn
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import pymysql
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
        SELECT user_id, username, nickname, phone, email, role_id, password
        FROM users
        WHERE (email = %s OR phone = %s)
          AND deleted_at IS NULL
        LIMIT 1
    """
    cur.execute(sql, (identifier, identifier))
    user = cur.fetchone()

    if user:
        stored_password = user['password']
        
        # ตรวจสอบว่า stored_password ใช้ hash method ที่รองรับ (เช่น bcrypt)
        if stored_password and check_password_hash(stored_password, password):
            return user
        else:
            return None  # รหัสผ่านไม่ตรงกัน

    return None  # หากไม่พบผู้ใช้

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
    hashed_password = generate_password_hash(new_password, method='bcrypt')

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


def register_user(username, nickname, phone, email, password, role_id):
    conn = get_conn()
    cur = conn.cursor()

    # แฮชรหัสผ่านด้วย bcrypt
    hashed_password = generate_password_hash(password, method='bcrypt')

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






