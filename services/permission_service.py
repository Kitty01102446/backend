from services.db import get_conn

# ============================================================
#                     SELECT ALL PERMISSION
# ============================================================
def get_all_permission():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT PERMISSION BY ID
# ============================================================
def get_permission_by_id(pid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM permission WHERE permission_id=%s", (pid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT PERMISSION
# ============================================================
def insert_permission(code: str, name: str):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO permission (code, name, created_at)
        VALUES (%s, %s, NOW())
    """

    cur.execute(sql, (code, name))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                      UPDATE PERMISSION
# ============================================================
def update_permission(pid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE permission
        SET code=%s,
            name=%s,
            updated_at = NOW()
        WHERE permission_id=%s
    """

    cur.execute(sql, (
        data.get("code"),
        data.get("name"),
        pid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                      DELETE PERMISSION
# ============================================================
def delete_permission(pid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM permission WHERE permission_id=%s", (pid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
