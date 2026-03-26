from services.db import get_conn

# ============================================================
#                     SELECT ALL STATUS_STORE
# ============================================================
def get_all_status_store():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                SELECT STATUS_STORE BY ID
# ============================================================
def get_status_store_by_id(sid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM status_store WHERE status_store_id=%s", (sid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                     INSERT STATUS_STORE
# ============================================================
def insert_status_store(status_store_name: str, description: str):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO status_store (status_store_name, description, created_at)
        VALUES (%s, %s, NOW())
    """

    cur.execute(sql, (status_store_name, description))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                     UPDATE STATUS_STORE
# ============================================================
def update_status_store(sid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE status_store
        SET status_store_name=%s,
            description=%s
        WHERE status_store_id=%s
    """

    cur.execute(sql, (
        data.get("status_store_name"),
        data.get("description"),
        sid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                     DELETE STATUS_STORE
# ============================================================
def delete_status_store(sid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM status_store WHERE status_store_id=%s", (sid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
