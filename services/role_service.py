from services.db import get_conn

# ============================================================
#                     SELECT ALL ROLE
# ============================================================
def get_all_role():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT ROLE BY ID
# ============================================================
def get_role_by_id(rid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM role WHERE role_id=%s", (rid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT ROLE
# ============================================================
def insert_role(role_name: str, description: str):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO role (role_name, description, created_at)
        VALUES (%s, %s, NOW())
    """

    cur.execute(sql, (role_name, description))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                      UPDATE ROLE
# ============================================================
def update_role(rid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE role
        SET role_name=%s,
            description=%s
        WHERE role_id=%s
    """

    cur.execute(sql, (
        data.get("role_name"),
        data.get("description"),
        rid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                      DELETE ROLE
# ============================================================
def delete_role(rid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM role WHERE role_id=%s", (rid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
