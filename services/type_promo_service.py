from services.db import get_conn

# ============================================================
#                SELECT ALL TYPE_PROMO
# ============================================================
def get_all_type_promos():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                SELECT TYPE_PROMO BY ID
# ============================================================
def get_type_promo_by_id(tid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM type_promo WHERE type_promo_id=%s", (tid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                INSERT TYPE_PROMO
# ============================================================
def insert_type_promo(name: str, description: str):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO type_promo (name, description)
        VALUES (%s, %s)
    """

    cur.execute(sql, (name, description))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                UPDATE TYPE_PROMO
# ============================================================
def update_type_promo(tid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE type_promo
        SET name=%s,
            description=%s
        WHERE type_promo_id=%s
    """

    cur.execute(sql, (
        data.get("name"),
        data.get("description"),
        tid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                DELETE TYPE_PROMO
# ============================================================
def delete_type_promo(tid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM type_promo WHERE type_promo_id=%s", (tid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
