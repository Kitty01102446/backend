from services.db import get_conn

# ============================================================
#                     SELECT ALL REVIEW
# ============================================================
def get_all_review():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            r.review_id,
            r.rating,
            r.comment,
            r.user_id,
            r.store_id,
            r.created_at,
            COALESCE(NULLIF(u.nickname, ''), NULLIF(u.username, ''), u.email, CONCAT('User #', r.user_id)) AS customer_name
        FROM review r
        LEFT JOIN users u ON r.user_id = u.user_id
        ORDER BY r.created_at DESC, r.review_id DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_reviews_by_store(store_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            r.review_id,
            r.rating,
            r.comment,
            r.user_id,
            r.store_id,
            r.created_at,
            COALESCE(NULLIF(u.nickname, ''), NULLIF(u.username, ''), u.email, CONCAT('User #', r.user_id)) AS customer_name
        FROM review r
        LEFT JOIN users u ON r.user_id = u.user_id
        WHERE r.store_id = %s
        ORDER BY r.created_at DESC, r.review_id DESC
    """, (store_id,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT REVIEW BY ID
# ============================================================
def get_review_by_id(rid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM review WHERE review_id=%s", (rid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT REVIEW
# ============================================================
def insert_review(rating: int, comment: str, user_id: int, store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO review (rating, comment, user_id, store_id, created_at)
        VALUES (%s, %s, %s, %s, NOW())
    """

    cur.execute(sql, (rating, comment, user_id, store_id))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                      UPDATE REVIEW
# ============================================================
def update_review(rid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE review
        SET rating=%s,
            comment=%s,
            user_id=%s,
            store_id=%s,
            updated_at = NOW()
        WHERE review_id=%s
    """

    cur.execute(sql, (
        data.get("rating"),
        data.get("comment"),
        data.get("user_id"),
        data.get("store_id"),
        rid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                      DELETE REVIEW
# ============================================================
def delete_review(rid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM review WHERE review_id=%s", (rid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
