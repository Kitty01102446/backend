from services.db import get_conn

# ============================================================
#                SELECT ALL STORE ADDRESS
# ============================================================
import pymysql

import pymysql

def get_all_store_address():
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    sql = """
        SELECT
            sa.store_address_id,

            s.store_id,
            s.store_name,

            sa.province,
            sa.district,
            sa.subdistrict,
            sa.postal_code,
            sa.street,
            sa.is_verified,
            sa.has_parking,
            TIME_FORMAT(sa.open_time, '%H:%i:%s') AS open_time,
            TIME_FORMAT(sa.close_time, '%H:%i:%s') AS close_time,
            sa.recommend_text,

            -- TAG
            t.tag_id,
            t.tag_name,

            -- SERVICE
            sv.service_id,
            sv.service_name,
            sv.price,
            sv.duration_minutes,
            sv.description,
            sv.type_id
        FROM store_address sa

        JOIN store s 
            ON sa.store_id = s.store_id

        LEFT JOIN store_tag st
            ON s.store_id = st.store_id
        LEFT JOIN tag t
            ON st.tag_id = t.tag_id

        LEFT JOIN service sv
            ON s.store_id = sv.store_id

        WHERE sa.deleted_at IS NULL
          AND s.deleted_at IS NULL

        ORDER BY sa.store_address_id, sv.service_id, t.tag_id
    """

    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# ============================================================
#                SELECT STORE ADDRESS BY ID
# ============================================================
def get_store_address_by_id(sid: int):
    conn = get_conn()
    # แนะนำให้ใช้ dictionary=True เพื่อให้ React ดึงข้อมูลผ่านชื่อ key ได้ง่ายขึ้น
    cur = conn.cursor() 

    sql = """
        SELECT
            store_address_id,
            province,
            district,
            subdistrict,
            postal_code,
            street,
            store_id,
            is_verified,
            has_parking,
            TIME_FORMAT(open_time, '%%H:%%i:%%s') AS open_time,
            TIME_FORMAT(close_time, '%%H:%%i:%%s') AS close_time,
            recommend_text,
            latitude,
            longitude
        FROM store_address
        WHERE store_address_id = %s
          AND deleted_at IS NULL
    """

    cur.execute(sql, (sid,))
    row = cur.fetchone()

    cur.close()
    conn.close()
    return row
# ============================================================
#                INSERT STORE ADDRESS
# ============================================================
def _geocode_from_data(data: dict):
    """แปลงที่อยู่จากฟิลด์ province/district/subdistrict/street เป็นพิกัดอัตโนมัติ"""
    from services.geocode_service import geocode_address

    full_address = ", ".join(
        part for part in [
            data.get("street"),
            data.get("subdistrict"),
            data.get("district"),
            data.get("province"),
        ] if part
    )
    return geocode_address(full_address)


def insert_store_address(data: dict):
    conn = get_conn()
    cur = conn.cursor()

    latitude, longitude = _geocode_from_data(data)

    sql = """
        INSERT INTO store_address (
            province,
            district,
            subdistrict,
            postal_code,
            street,
            store_id,
            is_verified,
            has_parking,
            open_time,
            close_time,
            recommend_text,
            latitude,
            longitude
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """

    cur.execute(sql, (
        data.get("province"),
        data.get("district"),
        data.get("subdistrict"),
        data.get("postal_code"),
        data.get("street"),
        data.get("store_id"),
        data.get("is_verified", 0),
        data.get("has_parking", 0),
        data.get("open_time"),
        data.get("close_time"),
        data.get("recommend_text"),
        latitude,
        longitude,
    ))

    conn.commit()
    new_id = cur.lastrowid

    cur.close()
    conn.close()
    return new_id

# ============================================================
#                UPDATE STORE ADDRESS
# ============================================================
def update_store_address(sid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    latitude, longitude = _geocode_from_data(data)

    sql = """
        UPDATE store_address
        SET province=%s,
            district=%s,
            subdistrict=%s,
            postal_code=%s,
            street=%s,
            is_verified=%s,
            has_parking=%s,
            open_time=%s,
            close_time=%s,
            recommend_text=%s,
            latitude=%s,
            longitude=%s
        WHERE store_address_id=%s
          AND deleted_at IS NULL
    """

    cur.execute(sql, (
        data.get("province"),
        data.get("district"),
        data.get("subdistrict"),
        data.get("postal_code"),
        data.get("street"),
        data.get("is_verified", 0),
        data.get("has_parking", 0),
        data.get("open_time"),
        data.get("close_time"),
        data.get("recommend_text"),
        latitude,
        longitude,
        sid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated

# ============================================================
#                UPDATE PIN (LAT/LNG) BY STORE_ID
# ============================================================
def update_store_location(store_id: int, latitude: float, longitude: float):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE store_address
        SET latitude=%s, longitude=%s
        WHERE store_id=%s
          AND deleted_at IS NULL
    """

    cur.execute(sql, (latitude, longitude, store_id))
    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated

# ============================================================
#                DELETE STORE ADDRESS
# ============================================================
def delete_store_address(sid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE store_address
        SET deleted_at = NOW()
        WHERE store_address_id = %s
    """

    cur.execute(sql, (sid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted


