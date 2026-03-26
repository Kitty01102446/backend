from services.db import get_conn

# ============================================================
#                     SELECT ALL EMPLOYEES
# ============================================================
def get_all_employees():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee where deleted_at is null")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT EMPLOYEE BY ID
# ============================================================
def get_employee_by_id(eid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM employee WHERE employee_id=%s", (eid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT EMPLOYEE
# ============================================================
def insert_employee(fullname: str, phone: str, email: str, position: str, store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO employee (fullname, phone, email, position, store_id)
        VALUES (%s, %s, %s, %s, %s)
    """

    cur.execute(sql, (fullname, phone, email, position, store_id))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id

# ============================================================
#                      UPDATE EMPLOYEE
# ============================================================
def update_employee(eid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE employee
        SET fullname=%s,
            phone=%s,
            position=%s,
            store_id=%s
        WHERE employee_id=%s
    """

    cur.execute(sql, (
        data.get("fullname"),
        data.get("phone"),
        data.get("position"),
        data.get("store_id"),
        eid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                     DELETE EMPLOYEE (HARD DELETE)
# ============================================================
def delete_employee(eid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
    UPDATE employee
    SET deleted_at = NOW()
    WHERE employee_id = %s
"""

    cur.execute(sql, (eid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted



# ============================================================
#        SELECT EMPLOYEE BY STORE ID   ✅ เพิ่มอันนี้
# ============================================================
def get_employee_by_store_id(store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT 
            employee_id,
            fullname,
            phone,
            email,
            position,
            DATE_FORMAT(created_at, '%%d/%%m/%%Y') AS start_date
        FROM employee
        WHERE store_id = %s
          AND deleted_at IS NULL
        ORDER BY employee_id DESC
    """

    cur.execute(sql, (store_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows



# ============================================================
#   GET EMPLOYEE BY STORE
# ============================================================
def get_employees_by_store(store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            employee_id,
            fullname,
            phone,
            email,
            position,
            DATE_FORMAT(created_at, '%%d/%%m/%%Y') AS start_date
        FROM employee
        WHERE store_id = %s
          AND deleted_at IS NULL
        ORDER BY employee_id DESC
    """, (store_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows