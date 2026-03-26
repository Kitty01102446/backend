from services.db import get_conn

# ============================================================
#                     SELECT ALL FAVORITE
# ============================================================
def get_all_favorite():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT FAVORITE BY ID
# ============================================================
def get_favorite_by_id(fid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM favorite WHERE favorite_id=%s", (fid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT FAVORITE
# ============================================================
def insert_favorite(user_id: int, store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO favorite (user_id, store_id, created_at, updated_at)
        VALUES (%s, %s, NOW(), NOW())
    """

    cur.execute(sql, (user_id, store_id))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                      UPDATE FAVORITE
# ============================================================
def update_favorite(fid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE favorite
        SET user_id=%s,
            store_id=%s,
            updated_at = NOW()
        WHERE favorite_id=%s
    """

    cur.execute(sql, (
        data.get("user_id"),
        data.get("store_id"),
        fid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                  DELETE FAVORITE
# ============================================================
def delete_favorite(fid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute(sql, (fid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
