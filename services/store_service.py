from services.db import get_conn

# ============================================================
#           STORE_ID ทั้งหมดที่ user คนนี้เป็นเจ้าของ (ใช้ตรวจสิทธิ์ Admin)
# ============================================================
def get_store_ids_owned_by_user(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT store_id FROM store WHERE user_id=%s AND deleted_at IS NULL",
        (user_id,)
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [r["store_id"] for r in rows]


# ============================================================
#   USER_ID เจ้าของร้าน (ใช้หาผู้รับ Notification ฝั่งร้าน)
# ============================================================
def get_store_owner_user_id(store_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT user_id, store_name FROM store WHERE store_id=%s AND deleted_at IS NULL",
        (store_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


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
  AND (store.status_store_id IS NULL OR store.status_store_id NOT IN (4, 5))
GROUP BY store.store_id

    """)  # คำสั่ง SQL
    rows = cur.fetchall()  # ดึงข้อมูลทั้งหมดที่ได้จาก query

    # ดึงที่อยู่ (จังหวัด/อำเภอ/ตำบล/ถนน) แยกต่างหาก -- ใช้สำหรับช่อง "สถานที่"
    # ในแถบค้นหาของหน้าแรก ไม่ join รวมกับ query ข้างบนเพราะจะทำให้ COUNT/AVG ของ
    # รีวิวเพี้ยน (store_address เป็น 1:1 กับร้านอยู่แล้วแต่กันเหนียวไว้)
    cur.execute("""
        SELECT store_id, province, district, subdistrict, street
        FROM store_address
        WHERE deleted_at IS NULL
    """)
    address_by_store = {r["store_id"]: r for r in cur.fetchall()}

    # ดึงรายชื่อบริการของแต่ละร้าน (รวมเป็นสตริงเดียวคั่นด้วย "||") -- ใช้สำหรับ
    # ช่อง "บริการ" ในแถบค้นหาของหน้าแรก
    cur.execute("""
        SELECT store_id, GROUP_CONCAT(DISTINCT service_name SEPARATOR '||') AS service_names
        FROM service
        WHERE store_id IS NOT NULL
        GROUP BY store_id
    """)
    services_by_store = {r["store_id"]: r["service_names"] for r in cur.fetchall()}

    for row in rows:
        addr = address_by_store.get(row["store_id"]) or {}
        row["province"] = addr.get("province")
        row["district"] = addr.get("district")
        row["subdistrict"] = addr.get("subdistrict")
        row["street"] = addr.get("street")
        row["service_names"] = services_by_store.get(row["store_id"]) or ""

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
            sa.latitude,
            sa.longitude,

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


# ============================================================
#                     GET NEARBY STORES
# ============================================================
from datetime import datetime, time as dtime, timedelta


def _to_time(value):
    """แปลงค่า open_time/close_time (timedelta หรือ str) ให้เป็น datetime.time"""
    if isinstance(value, timedelta):
        total_seconds = int(value.total_seconds())
        h, rem = divmod(total_seconds, 3600)
        m, s = divmod(rem, 60)
        return dtime(hour=h % 24, minute=m, second=s)
    if isinstance(value, str):
        try:
            h, m, s = (value.split(":") + ["0", "0"])[:3]
            return dtime(hour=int(h) % 24, minute=int(m), second=int(s))
        except ValueError:
            return None
    return None


def _normalize(values, invert=False):
    """min-max normalize เป็นช่วง 0-1, ค่าที่เท่ากันหมดจะได้ 1 ทั้งหมด"""
    lo, hi = min(values), max(values)
    if hi == lo:
        return [1.0 for _ in values]
    return [
        (hi - v) / (hi - lo) if invert else (v - lo) / (hi - lo)
        for v in values
    ]


def get_nearby_stores(lat=None, lng=None, province=None, radius_km=5, limit=20):
    conn = get_conn()
    cur = conn.cursor()

    use_distance = lat is not None and lng is not None

    base_select = """
        SELECT
            s.store_id,
            s.store_name,
            s.image,
            s.price,
            s.status_store_id,
            sa.store_address_id,
            sa.province,
            sa.district,
            sa.subdistrict,
            sa.street,
            sa.open_time,
            sa.close_time,
            sa.latitude,
            sa.longitude,
            COALESCE(rv.avg_rating, 0) AS avg_rating,
            COALESCE(rv.review_count, 0) AS review_count,
            COALESCE(emp.employee_count, 0) AS employee_count,
            COALESCE(bk.booked_today, 0) AS booked_today,
            COALESCE(cl.click_count, 0) AS click_count
    """

    joins = """
        FROM store s
        JOIN store_address sa ON sa.store_id = s.store_id AND sa.deleted_at IS NULL
        LEFT JOIN (
            SELECT store_id, AVG(rating) AS avg_rating, COUNT(*) AS review_count
            FROM review
            GROUP BY store_id
        ) rv ON rv.store_id = s.store_id
        LEFT JOIN (
            SELECT store_id, COUNT(*) AS employee_count
            FROM employee
            WHERE deleted_at IS NULL
            GROUP BY store_id
        ) emp ON emp.store_id = s.store_id
        LEFT JOIN (
            SELECT store_id, COUNT(*) AS booked_today
            FROM bookings
            WHERE booking_date = CURDATE()
              AND status_booking_id != 4
              AND deleted_at IS NULL
            GROUP BY store_id
        ) bk ON bk.store_id = s.store_id
        LEFT JOIN (
            SELECT store_id, COUNT(*) AS click_count
            FROM click_log
            WHERE deleted_at IS NULL
            GROUP BY store_id
        ) cl ON cl.store_id = s.store_id
        WHERE s.deleted_at IS NULL
          AND (s.status_store_id IS NULL OR s.status_store_id NOT IN (4, 5))
    """

    params = []

    if use_distance:
        base_select += """,
            (6371 * ACOS(
                COS(RADIANS(%s)) * COS(RADIANS(sa.latitude)) *
                COS(RADIANS(sa.longitude) - RADIANS(%s)) +
                SIN(RADIANS(%s)) * SIN(RADIANS(sa.latitude))
            )) AS distance_km
        """
        params += [lat, lng, lat]
        joins += " AND sa.latitude IS NOT NULL AND sa.longitude IS NOT NULL"
        sql = base_select + joins + " HAVING distance_km <= %s"
        params.append(radius_km)
    else:
        base_select += ", NULL AS distance_km"
        sql = base_select + joins
        if province:
            sql += " AND sa.province = %s"
            params.append(province)

    cur.execute(sql, tuple(params))
    rows = list(cur.fetchall())
    cur.close()
    conn.close()

    now_t = datetime.now().time()
    for row in rows:
        row["available_slots"] = max(row["employee_count"] - row["booked_today"], 0)
        row["avg_rating"] = float(row["avg_rating"])
        open_t = _to_time(row.get("open_time"))
        close_t = _to_time(row.get("close_time"))
        row["is_open"] = bool(
            row["status_store_id"] == 1 and open_t and close_t and open_t <= now_t <= close_t
        )
        if row.get("distance_km") is not None:
            row["distance_km"] = round(float(row["distance_km"]), 2)
        row["open_time"] = str(row["open_time"]) if row.get("open_time") is not None else None
        row["close_time"] = str(row["close_time"]) if row.get("close_time") is not None else None
        row.pop("employee_count", None)
        row.pop("booked_today", None)

    if use_distance and rows:
        distances = [r["distance_km"] for r in rows]
        slots = [r["available_slots"] for r in rows]
        ratings = [r["avg_rating"] for r in rows]
        clicks = [r["click_count"] for r in rows]

        distance_scores = _normalize(distances, invert=True)
        slot_scores = _normalize(slots)
        rating_scores = _normalize(ratings)
        popularity_scores = _normalize(clicks)

        for row, d, sl, rt, pop in zip(rows, distance_scores, slot_scores, rating_scores, popularity_scores):
            row["score"] = round(0.4 * d + 0.3 * sl + 0.2 * rt + 0.1 * pop, 4)

        rows.sort(key=lambda r: r["score"], reverse=True)
    else:
        rows.sort(key=lambda r: (r["avg_rating"], r["click_count"]), reverse=True)

    return rows[:limit]


