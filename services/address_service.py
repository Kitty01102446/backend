from services.db import get_conn

# ============================================================
#                     SELECT ALL ADDRESS
# ============================================================
def get_all_address():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT ADDRESS BY ID
# ============================================================
def get_address_by_id(aid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address WHERE address_id=%s", (aid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# =========================================f===================
#                      INSERT ADDRESS
# ============================================================
def insert_address(province: str, district: str, subdistrict: str,
                   postal_code: str, user_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO address (province, district, subdistrict, postal_code, user_id, created_at, updated_at)
        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
    """

    cur.execute(sql, (province, district, subdistrict, postal_code, user_id))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                      UPDATE ADDRESS
# ============================================================
def update_address(aid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE address
        SET province=%s,
            district=%s,
            subdistrict=%s,
            postal_code=%s,
            user_id=%s,
            updated_at = NOW()
        WHERE address_id=%s
    """

    cur.execute(sql, (
        data.get("province"),
        data.get("district"),
        data.get("subdistrict"),
        data.get("postal_code"),
        data.get("user_id"),
        aid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                     DELETE ADDRESS (NO SOFT DELETE)
# ============================================================
def delete_address(aid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute(sql, (aid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
