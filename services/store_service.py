from services.db import get_conn

# ============================================================
#                     SELECT ALL STORES
# ============================================================
def get_all_store():
    conn = get_conn()  # เชื่อมต่อกับฐานข้อมูล
    cur = conn.cursor()  # สร้าง cursor สำหรับการ query
    # คำสั่ง SQL ที่ใช้ JOIN ระหว่าง store และ review
    cur.execute("""
        SELECT
  store.store_id,
  store.store_name,
  store.phone,
  store.email,
  store.address,
  store.image,
  store.price,
  COUNT(review.review_id) AS review_count,
  AVG(review.rating) AS avg_rating
FROM store
LEFT JOIN review ON store.store_id = review.store_id
WHERE store.deleted_at IS NULL
GROUP BY store.store_id

    """)  # คำสั่ง SQL
    rows = cur.fetchall()  # ดึงข้อมูลทั้งหมดที่ได้จาก query
    cur.close()  # ปิด cursor
    conn.close()  # ปิดการเชื่อมต่อฐานข้อมูล
    return rows  # คืนค่าผลลัพธ์ที่ได้

# ============================================================
#                     SELECT STORE BY ID
# ============================================================
from datetime import timedelta

def get_store_by_id(sid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT 
            s.*,

            sa.recommend_text,
            sa.open_time,
            sa.close_time,

            ser.service_id,
            ser.service_name,
            ser.price AS service_price,
            ser.duration_minutes

        FROM store s
        LEFT JOIN store_address sa 
            ON s.store_id = sa.store_id
        LEFT JOIN service ser 
            ON s.store_id = ser.store_id
        WHERE s.store_id = %s
          AND s.deleted_at IS NULL
    """

    cur.execute(sql, (sid,))
    rows = cur.fetchall()

    cur.close()
    conn.close()

    # 🔥 แปลง timedelta เป็น string
    for row in rows:
        if isinstance(row.get("open_time"), timedelta):
            row["open_time"] = str(row["open_time"])

        if isinstance(row.get("close_time"), timedelta):
            row["close_time"] = str(row["close_time"])

        if isinstance(row.get("duration_minutes"), timedelta):
            row["duration_minutes"] = str(row["duration_minutes"])

    return rows
# ============================================================
#                     INSERT STORE
# ============================================================
def insert_store(store_name: str, phone: str, email: str, address: str,
                 image: str, status_store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO store
            (store_name, phone, email, address, image, status_store_id, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """

    cur.execute(sql, (store_name, phone, email, address, image, status_store_id))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                     UPDATE STORE
# ============================================================
def update_store(sid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE store
        SET store_name=%s,
            phone=%s,
            email=%s,
            address=%s,
            image=%s,
            status_store_id=%s,
            updated_at = NOW()
        WHERE store_id=%s
    """

    cur.execute(sql, (
        data.get("store_name"),
        data.get("phone"),
        data.get("email"),
        data.get("address"),
        data.get("image"),
        data.get("status_store_id"),
        sid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated

def update_store(sid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE store
        SET store_name=%s,
            phone=%s,
            email=%s,
            address=%s,
            recommend_text=%s,
            open_time=%s,
            close_time=%s,
            image=%s,
            price=%s,
            status_store_id=%s,
            updated_at = NOW()
        WHERE store_id=%s
    """

    cur.execute(sql, (
        data.get("store_name"),
        data.get("phone"),
        data.get("email"),
        data.get("address"),
        data.get("recommend_text"),
        data.get("open_time"),
        data.get("close_time"),
        data.get("image"),
        data.get("price"),
        data.get("status_store_id"),
        sid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                     DELETE STORE
# ============================================================
def delete_store(sid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM store WHERE store_id=%s", (sid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted


