from services.db import get_conn

# ============================================================
#                     SELECT ALL PAYMENT
# ============================================================
def get_all_payment():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT PAYMENT BY ID
# ============================================================
def get_payment_by_id(pid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM payment WHERE payment_id=%s", (pid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT PAYMENT
# ============================================================
def insert_payment(method: str, payment_date: str, amount: float,
                   booking_id: int, bill_id: int):

    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO payment (method, payment_date, amount, booking_id, bill_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    cur.execute(sql, (method, payment_date, amount, booking_id, bill_id))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                      UPDATE PAYMENT
# ============================================================
def update_payment(pid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE payment
        SET method=%s,
            payment_date=%s,
            amount=%s,
            booking_id=%s,
            bill_id=%s
        WHERE payment_id=%s
    """

    cur.execute(sql, (
        data.get("method"),
        data.get("payment_date"),
        data.get("amount"),
        data.get("booking_id"),
        data.get("bill_id"),
        pid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                      DELETE PAYMENT
# ============================================================
def delete_payment(pid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM payment WHERE payment_id=%s", (pid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
