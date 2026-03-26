from services.db import get_conn

# ============================================================
#                     SELECT ALL BILL
# ============================================================
def get_all_bill():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM address where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT BILL BY ID
# ============================================================
def get_bill_by_id(bid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM bill WHERE bill_id=%s", (bid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT BILL
# ============================================================
def insert_bill(total_amount: float, store_id: int, status_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO bill (total_amount, store_id, status_id)
        VALUES (%s, %s, %s)
    """

    cur.execute(sql, (total_amount, store_id, status_id))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                      UPDATE BILL
# ============================================================
def update_bill(bid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE bill
        SET total_amount=%s,
            store_id=%s,
            status_id=%s
        WHERE bill_id=%s
    """

    cur.execute(sql, (
        data.get("total_amount"),
        data.get("store_id"),
        data.get("status_id"),
        bid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                      DELETE BILL
# ============================================================
def delete_bill(bid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM bill WHERE bill_id=%s", (bid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
