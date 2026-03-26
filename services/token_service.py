from services.db import get_conn

# ============================================================
#                     SELECT ALL TOKENS
# ============================================================
def get_all_tokens():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                     SELECT TOKEN BY ID
# ============================================================
def get_token_by_id(tid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM token WHERE token_id=%s", (tid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                     INSERT TOKEN
# ============================================================
def insert_token(jwt_key: str, user_id: int, expired_at: str):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO token (jwt_key, user_id, created_at, expired_at)
        VALUES (%s, %s, NOW(), %s)
    """

    cur.execute(sql, (jwt_key, user_id, expired_at))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                     UPDATE TOKEN
# ============================================================
def update_token(tid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE token
        SET jwt_key=%s,
            user_id=%s,
            expired_at=%s
        WHERE token_id=%s
    """

    cur.execute(sql, (
        data.get("jwt_key"),
        data.get("user_id"),
        data.get("expired_at"),
        tid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                     DELETE TOKEN
# ============================================================
def delete_token(tid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM token WHERE token_id=%s", (tid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
