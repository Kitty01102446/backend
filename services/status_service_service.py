from services.db import get_conn

# ============================================================
#                 SELECT ALL STATUS_SERVICE
# ============================================================
def get_all_status_service():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#               SELECT STATUS_SERVICE BY ID
# ============================================================
def get_status_service_by_id(sid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM status_service WHERE status_service_id=%s", (sid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                 INSERT STATUS_SERVICE
# ============================================================
def insert_status_service(status_service_name: str, description: str):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO status_service (status_service_name, description, created_at)
        VALUES (%s, %s, NOW())
    """

    cur.execute(sql, (status_service_name, description))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                 UPDATE STATUS_SERVICE
# ============================================================
def update_status_service(sid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE status_service
        SET status_service_name=%s,
            description=%s
        WHERE status_service_id=%s
    """

    cur.execute(sql, (
        data.get("status_service_name"),
        data.get("description"),
        sid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                 DELETE STATUS_SERVICE
# ============================================================
def delete_status_service(sid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM status_service WHERE status_service_id=%s", (sid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
