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
#                  SELECT EMPLOYEE BY USER_ID (บัญชี login ของช่าง)
# ============================================================
def get_employee_by_user_id(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT * FROM employee WHERE user_id=%s AND deleted_at IS NULL",
        (user_id,)
    )
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                  ผูกบัญชี login (users.user_id) ให้ช่างคนนี้
# ============================================================
def set_employee_user_id(employee_id: int, user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE employee SET user_id=%s WHERE employee_id=%s AND deleted_at IS NULL",
        (user_id, employee_id)
    )
    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated


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
            e.employee_id,
            e.fullname,
            e.phone,
            e.email,
            e.position,
            e.user_id,
            DATE_FORMAT(e.created_at, '%%d/%%m/%%Y') AS start_date,
            e.current_status_id,
            se.status_employee_name,
            e.base_salary,
            e.commission_rate
        FROM employee e
        LEFT JOIN status_employee se ON se.status_employee_id = e.current_status_id
        WHERE e.store_id = %s
          AND e.deleted_at IS NULL
        ORDER BY e.employee_id DESC
    """

    cur.execute(sql, (store_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


# ============================================================
#   GET EMPLOYEE BY STORE -- ฉบับสาธารณะ (ไม่ต้อง login)
#   ใช้กับหน้าจองของลูกค้า ให้เลือกช่างได้ -- คืนเฉพาะฟิลด์ที่ไม่อ่อนไหว
#   (ไม่มีเบอร์โทร/อีเมล/เงินเดือน/commission เหมือน get_employee_by_store_id)
# ============================================================
def get_public_employees_by_store(store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT employee_id, fullname, position
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
            e.employee_id,
            e.fullname,
            e.phone,
            e.email,
            e.position,
            e.user_id,
            DATE_FORMAT(e.created_at, '%%d/%%m/%%Y') AS start_date,
            e.current_status_id,
            se.status_employee_name,
            e.base_salary,
            e.commission_rate
        FROM employee e
        LEFT JOIN status_employee se ON se.status_employee_id = e.current_status_id
        WHERE e.store_id = %s
          AND e.deleted_at IS NULL
        ORDER BY e.employee_id DESC
    """, (store_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows