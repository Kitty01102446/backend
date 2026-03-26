from services.db import get_conn

# ============================================================
#                     SELECT ALL ROLE_PERMISSION
# ============================================================
def get_all_role_permission():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT ROLE_PERMISSION BY ID
# ============================================================
def get_role_permission_by_id(rpid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM role_permission WHERE role_permission_id=%s", (rpid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT ROLE_PERMISSION
# ============================================================
def insert_role_permission(permission_id: int, role_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO role_permission (permission_id, role_id, created_at)
        VALUES (%s, %s, NOW())
    """

    cur.execute(sql, (permission_id, role_id))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                      UPDATE ROLE_PERMISSION
# ============================================================
def update_role_permission(rpid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE role_permission
        SET permission_id=%s,
            role_id=%s
        WHERE role_permission_id=%s
    """

    cur.execute(sql, (
        data.get("permission_id"),
        data.get("role_id"),
        rpid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                      DELETE ROLE_PERMISSION
# ============================================================
def delete_role_permission(rpid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM role_permission WHERE role_permission_id=%s", (rpid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
