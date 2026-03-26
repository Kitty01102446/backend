from services.db import get_conn

# ============================================================
#                SELECT ALL TYPE_BOOKING
# ============================================================
def get_all_type_bookings():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                SELECT TYPE_BOOKING BY ID
# ============================================================
def get_type_booking_by_id(tid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM type_booking WHERE type_booking_id=%s", (tid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                INSERT TYPE_BOOKING
# ============================================================
def insert_type_booking(type_booking_name: str, description: str):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO type_booking (type_booking_name, description)
        VALUES (%s, %s)
    """

    cur.execute(sql, (type_booking_name, description))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                UPDATE TYPE_BOOKING
# ============================================================
def update_type_booking(tid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE type_booking
        SET type_booking_name=%s,
            description=%s
        WHERE type_booking_id=%s
    """

    cur.execute(sql, (
        data.get("type_booking_name"),
        data.get("description"),
        tid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                DELETE TYPE_BOOKING
# ============================================================
def delete_type_booking(tid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM type_booking WHERE type_booking_id=%s", (tid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
