from services.db import get_conn

# ============================================================
#                SELECT ALL TYPE_SERVICE
# ============================================================
def get_all_type_services():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                SELECT TYPE_SERVICE BY ID
# ============================================================
def get_type_service_by_id(tid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM type_service WHERE type_id=%s", (tid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                INSERT TYPE_SERVICE
# ============================================================
def insert_type_service(name: str, description: str):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO type_service (name, description)
        VALUES (%s, %s)
    """

    cur.execute(sql, (name, description))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                UPDATE TYPE_SERVICE
# ============================================================
def update_type_service(tid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE type_service
        SET name=%s,
            description=%s
        WHERE type_id=%s
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
#                DELETE TYPE_SERVICE
# ============================================================
def delete_type_service(tid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM type_service WHERE type_id=%s", (tid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted


def get_all_type_services():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT type_id, name, description FROM type_service")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
