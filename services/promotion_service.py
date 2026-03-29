from services.db import get_conn

# ============================================================
#                     SELECT ALL PROMOTION
# ============================================================
def get_all_promotion():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM promotion
        WHERE deleted_at IS NULL
    """)

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

    cur.execute("""
        SELECT * FROM promotion
        WHERE promo_id=%s
        AND deleted_at IS NULL
    """, (pid,))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT PROMOTION
# ============================================================
def insert_promotion(name, detail, discount, store_id, type_promo_id, start_date, end_date, promo_code):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO promotion 
        (name, detail, discount, store_id, type_promo_id, start_date, end_date, promo_code, created_at, updated_at)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())
    """

    cur.execute(sql, (
        name,
        detail,
        discount,
        store_id,
        type_promo_id,
        start_date,
        end_date,
        promo_code
    ))

    conn.commit()
    new_id = cur.lastrowid

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
            detail=%s,
            discount=%s,
            store_id=%s,
            type_promo_id=%s,
            start_date=%s,
            end_date=%s,
            promo_code=%s,
            updated_at = NOW()
        WHERE promo_id=%s
    """

    cur.execute(sql, (
        data.get("name"),
        data.get("detail"),
        data.get("discount"),
        data.get("store_id"),
        data.get("type_promo_id"),
        data.get("start_date"),
        data.get("end_date"),
        data.get("promo_code"),
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

    sql = """
        UPDATE promotion
        SET deleted_at = NOW()
        WHERE promo_id = %s
        AND deleted_at IS NULL
    """

    cur.execute(sql, (pid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted


def get_promotion_by_store(store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT * FROM promotion
        WHERE store_id = %s
        AND deleted_at IS NULL
    """, (store_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
