from services.db import get_conn

# ============================================================
#                     SELECT ALL SERVICE
# ============================================================
def get_all_service():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT s.*, t.name as type_name
        FROM service s
        LEFT JOIN type_service t ON s.type_id = t.type_id
        ORDER BY s.service_id DESC
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT SERVICE BY ID
# ============================================================
def get_service_by_id(sid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM service WHERE service_id=%s", (sid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT SERVICE
# ============================================================
def insert_service(service_name: str, price: int, duration_minutes: int,
                   description: str, type_id: int, store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO service (service_name, price, duration_minutes, description,
                             type_id, store_id, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, NOW())
    """

    cur.execute(sql, (service_name, price, duration_minutes,
                      description, type_id, store_id))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                      UPDATE SERVICE
# ============================================================
def update_service(sid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE service
        SET service_name=%s,
            price=%s,
            duration_minutes=%s,
            description=%s,
            type_id=%s,
            store_id=%s
        WHERE service_id=%s
    """

    cur.execute(sql, (
        data.get("service_name"),
        data.get("price"),
        data.get("duration_minutes"),
        data.get("description"),
        data.get("type_id"),
        data.get("store_id"),
        sid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                      DELETE SERVICE
# ============================================================
def delete_service(sid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM service WHERE service_id=%s", (sid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted


# ============================================================
#            SELECT SERVICE BY STORE ID
# ============================================================
def get_services_by_store(store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT s.service_id,
               s.service_name,
               s.price,
               s.duration_minutes,
               s.description,
               s.type_id,
               t.name AS type_name
        FROM service s
        LEFT JOIN type_service t ON s.type_id = t.type_id
        WHERE s.store_id = %s
        ORDER BY s.service_id DESC
    """

    cur.execute(sql, (store_id,))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows

# ============================================================
#   SELECT BOOKINGS BY STORE ID
# ============================================================


# ============================================================
#   TOP SERVICES BY STORE
# ============================================================
def get_top_services_by_store(store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            bs.service_name,
            COUNT(bs.service_id) AS total_sales,
            SUM(bs.service_price) AS total_revenue
        FROM booking_services bs
        JOIN bookings b ON bs.booking_id = b.booking_id
        WHERE b.store_id = %s
          AND b.deleted_at IS NULL
        GROUP BY bs.service_name
        ORDER BY total_sales DESC
        LIMIT 5
    """, (store_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#   MONTHLY INCOME BY STORE
# ============================================================
def get_monthly_income_by_store(store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            DATE_FORMAT(booking_date, '%%Y-%%m') AS month,
            SUM(total_price) AS income
        FROM bookings
        WHERE store_id = %s
          AND deleted_at IS NULL
        GROUP BY DATE_FORMAT(booking_date, '%%Y-%%m')
        ORDER BY month ASC
    """, (store_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_monthly_income_by_store_year(store_id: int, year: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT 
            MONTH(booking_date) AS month_number,
            SUM(total_price) AS income
        FROM bookings
        WHERE store_id = %s
          AND YEAR(booking_date) = %s
          AND YEAR(booking_date) >= YEAR(CURDATE()) - 2
          AND deleted_at IS NULL
        GROUP BY MONTH(booking_date)
        ORDER BY month_number ASC
    """, (store_id, year))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows