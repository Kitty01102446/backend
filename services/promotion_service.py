from services.db import get_conn

# ============================================================
#                     SELECT ALL PROMOTION
# ============================================================
def get_all_promotion():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT PROMOTION BY ID
# ============================================================
def get_promotion_by_id(pid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM promotion WHERE promo_id=%s", (pid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT PROMOTION
# ============================================================
def insert_promotion(name: str, discount: int, store_id: int, type_promo_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO promotion (name, discount, store_id, type_promo_id, created_at)
        VALUES (%s, %s, %s, %s, NOW())
    """

    cur.execute(sql, (name, discount, store_id, type_promo_id))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                      UPDATE PROMOTION
# ============================================================
def update_promotion(pid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE promotion
        SET name=%s,
            discount=%s,
            store_id=%s,
            type_promo_id=%s,
            updated_at = NOW()
        WHERE promo_id=%s
    """

    cur.execute(sql, (
        data.get("name"),
        data.get("discount"),
        data.get("store_id"),
        data.get("type_promo_id"),
        pid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                      DELETE PROMOTION
# ============================================================
def delete_promotion(pid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM promotion WHERE promo_id=%s", (pid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
