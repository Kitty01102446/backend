from services.db import get_conn

# ============================================================
#                     SELECT ALL STATUS_BOOKING
# ============================================================
def get_all_status_booking():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT STATUS_BOOKING BY ID
# ============================================================
def get_status_booking_by_id(sid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM status_booking WHERE status_booking_id=%s", (sid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT STATUS_BOOKING
# ============================================================
def insert_status_booking(status_booking_name: str, description: str):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO status_booking (status_booking_name, description, created_at)
        VALUES (%s, %s, NOW())
    """

    cur.execute(sql, (status_booking_name, description))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                      UPDATE STATUS_BOOKING
# ============================================================
def update_status_booking(sid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE status_booking
        SET status_booking_name=%s,
            description=%s
        WHERE status_booking_id=%s
    """

    cur.execute(sql, (
        data.get("status_booking_name"),
        data.get("description"),
        sid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                      DELETE STATUS_BOOKING
# ============================================================
def delete_status_booking(sid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM status_booking WHERE status_booking_id=%s", (sid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
