from services.db import get_conn

# ============================================================
#                SELECT ALL CLICK_LOG
# ============================================================
def get_all_click_logs():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            cl.click_log_id,
            cl.user_id AS click_log_user_id,
            cl.store_id AS click_log_store_id,
            cl.created_at,
            cl.updated_at,
            cl.deleted_at,
            s.store_id,
            s.store_name,
            s.price,
            s.image,
            u.user_id,
            rv.rating,
            tg.tag
        FROM click_log cl
        JOIN store s
            ON cl.store_id = s.store_id
        JOIN users u
            ON cl.user_id = u.user_id
        LEFT JOIN (
            SELECT
                store_id,
                user_id,
                AVG(rating) AS rating
            FROM review
            GROUP BY store_id, user_id
        ) rv
            ON cl.store_id = rv.store_id
           AND cl.user_id = rv.user_id
        LEFT JOIN (
            SELECT
                st.store_id,
                GROUP_CONCAT(t.tag_name ORDER BY t.tag_name SEPARATOR ', ') AS tag
            FROM store_tag st
            JOIN tag t
                ON st.tag_id = t.tag_id
            GROUP BY st.store_id
        ) tg
            ON s.store_id = tg.store_id
        WHERE cl.deleted_at IS NULL
        ORDER BY cl.created_at DESC, cl.click_log_id DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# ============================================================
#                SELECT CLICK_LOG BY ID
# ============================================================
def get_click_log_by_id(cid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM click_log WHERE click_log_id=%s", (cid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                INSERT CLICK_LOG
# ============================================================
def insert_click_log(user_id: int, store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO click_log (user_id, store_id, created_at)
        VALUES (%s, %s, NOW())
    """

    cur.execute(sql, (user_id, store_id))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                UPDATE CLICK_LOG
# ============================================================
def update_click_log(cid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE click_log
        SET user_id=%s,
            store_id=%s,
            updated_at = NOW()
        WHERE click_log_id=%s
    """

    cur.execute(sql, (
        data.get("user_id"),
        data.get("store_id"),
        cid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                DELETE CLICK_LOG
# ============================================================
def delete_click_log(cid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM click_log WHERE click_log_id=%s", (cid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
