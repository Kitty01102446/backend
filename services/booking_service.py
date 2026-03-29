from services.db import get_conn
import pymysql



# ============================================================
#                     SELECT ALL BOOKINGS
# ============================================================
def get_all_booking():
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT
            booking_id,
            booking_date,
            TIME_FORMAT(booking_time, '%%H:%%i') AS booking_time,
            user_id,
            employee_id,
            store_id,
            type_booking_id,
            status_booking_id,
            total_price,
            total_minutes,
            created_at,
            updated_at
        FROM bookings
        WHERE deleted_at IS NULL
        ORDER BY booking_date, booking_time
    """)

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                  SELECT BOOKING BY ID
# ============================================================
def get_booking_by_id(bid: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT
            booking_id,
            booking_date,
            TIME_FORMAT(booking_time, '%%H:%%i') AS booking_time,
            user_id,
            employee_id,
            store_id,
            customer_name,
            customer_phone,
            customer_line,
            customer_email,
            customer_note,
            total_price,
            total_minutes,
            type_booking_id,
            status_booking_id,
            created_at,
            updated_at
        FROM bookings
        WHERE booking_id = %s
          AND deleted_at IS NULL
    """, (bid,))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                      INSERT BOOKING
# ============================================================
def insert_booking(data: dict):
    conn = get_conn()
    cur = conn.cursor()

    # 🔴 ตรวจสอบคิวซ้ำ
    if data.get("employee_id"):
        cur.execute("""
            SELECT booking_id
            FROM bookings
            WHERE employee_id = %s
              AND booking_date = %s
              AND booking_time = %s
              AND deleted_at IS NULL
        """, (
            data["employee_id"],
            data["booking_date"],
            data["booking_time"]
        ))

        exist = cur.fetchone()

        if exist:
            cur.close()
            conn.close()
            raise Exception("พนักงานมีคิวในเวลานี้แล้ว")

    sql = """
        INSERT INTO bookings (
          booking_date, booking_time,
          user_id, employee_id, store_id,
          customer_name, customer_phone,
          customer_line, customer_email, customer_note,
          total_price, total_minutes,
          type_booking_id, status_booking_id,
          created_at, updated_at
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NOW(),NOW())
    """

    cur.execute(sql, (
        data["booking_date"],
        data["booking_time"],
        data["user_id"],
        data.get("employee_id"),
        data["store_id"],

        data["customer"]["name"],
        data["customer"]["phone"],
        data["customer"].get("line"),
        data["customer"].get("email"),
        data["customer"].get("note"),

        data["total_price"],
        data["total_minutes"],

        data["type_booking_id"],
        data["status_booking_id"],
    ))

    booking_id = cur.lastrowid

    conn.commit()
    cur.close()
    conn.close()

    return booking_id


# ============================================================
#                      UPDATE BOOKING
# ============================================================
def update_booking(bid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    fields = []
    values = []

    allow_fields = [
        "booking_date",
        "booking_time",
        "employee_id",
        "store_id",
        "type_booking_id",
        "status_booking_id",
    ]

    for field in allow_fields:
        if field in data:
            fields.append(f"{field}=%s")
            values.append(data[field])

    if not fields:
        cur.close()
        conn.close()
        return False

    sql = f"""
        UPDATE bookings
        SET {', '.join(fields)},
            updated_at = NOW()
        WHERE booking_id = %s
          AND deleted_at IS NULL
    """

    values.append(bid)

    cur.execute(sql, tuple(values))
    conn.commit()

    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated


# ============================================================
#                  DELETE BOOKING (SOFT DELETE)
# ============================================================
def delete_booking(bid: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE bookings
        SET deleted_at = NOW()
        WHERE booking_id = %s
    """, (bid,))

    conn.commit()
    deleted = cur.rowcount > 0
    cur.close()
    conn.close()
    return deleted


# ============================================================
#               INSERT BOOKING SERVICES
# ============================================================
def insert_booking_services(booking_id: int, services: list):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO booking_services
        (booking_id, service_id, service_name, service_price, service_minutes)
        VALUES (%s,%s,%s,%s,%s)
    """

    for s in services:
        cur.execute(sql, (
            booking_id,
            s["service_id"],
            s["name"],
            s["price"],
            s["minutes"]
        ))

    conn.commit()
    cur.close()
    conn.close()


# ============================================================
#     SELECT BOOKING + SERVICES (DETAIL)
# ============================================================
def get_booking_with_services(bid: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT
            b.booking_id,
            b.booking_date,
            TIME_FORMAT(b.booking_time, '%%H:%%i') AS booking_time,

            b.customer_name,
            b.customer_phone,
            b.customer_email,

            bs.service_id,
            bs.service_name,
            bs.service_price,
            bs.service_minutes,

            b.total_price,
            b.total_minutes
        FROM bookings b
        JOIN booking_services bs ON b.booking_id = bs.booking_id
        WHERE b.booking_id = %s
          AND b.deleted_at IS NULL
    """, (bid,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#     SELECT BOOKINGS BY USER ID (ดึงการจองของผู้ใช้จาก user_id)
# ============================================================
def get_user_bookings(user_id: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    try:
        cur.execute("""
            SELECT 
                b.booking_id,
                DATE_FORMAT(b.booking_date, '%%Y-%%m-%%d') AS booking_date,
                TIME_FORMAT(b.booking_time, '%%H:%%i') AS booking_time,

                s.store_name,

                sb.status_booking_name,

                (SELECT GROUP_CONCAT(service_name SEPARATOR ', ')
                 FROM booking_services bs
                 WHERE bs.booking_id = b.booking_id) AS svc

            FROM bookings b

            LEFT JOIN store s 
                ON b.store_id = s.store_id

            LEFT JOIN status_booking sb
                ON b.status_booking_id = sb.status_booking_id

            WHERE b.user_id = %s
              AND b.deleted_at IS NULL

            ORDER BY b.booking_date DESC, b.booking_time DESC
        """, (user_id,))

        rows = cur.fetchall()
        return rows

    except Exception as e:
        print(f"Error: {e}")
        return []

    finally:
        cur.close()
        conn.close()

# ============================================================
#     SELECT BOOKINGS BY STORE ID
# ============================================================
def get_store_bookings(store_id: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT
            b.booking_id,
            DATE_FORMAT(b.booking_date, '%%d/%%m/%%Y') AS booking_date,
            TIME_FORMAT(b.booking_time, '%%H:%%i') AS booking_time,
            b.customer_name,
            b.user_id,
            b.total_price,
            sb.status_booking_name,
            e.fullname AS employee_name,

            GROUP_CONCAT(bs.service_name SEPARATOR ', ') AS services

        FROM bookings b
        LEFT JOIN employee e ON b.employee_id = e.employee_id
        LEFT JOIN status_booking sb ON b.status_booking_id = sb.status_booking_id
        LEFT JOIN booking_services bs ON b.booking_id = bs.booking_id

        WHERE b.store_id = %s
          AND b.deleted_at IS NULL

        GROUP BY b.booking_id
        ORDER BY b.booking_date DESC, b.booking_time DESC
    """, (store_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows



def update_booking_status_service(booking_id, status_id):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE bookings
        SET status_booking_id = %s,
            updated_at = NOW()
        WHERE booking_id = %s
          AND deleted_at IS NULL
    """, (status_id, booking_id))

    conn.commit()

    updated = cur.rowcount > 0

    cur.close()
    conn.close()

    return updated


# ============================================================
#   GET RECENT ALERTS BY STORE
# ============================================================
def get_recent_alerts_by_store(store_id: int):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT 
            booking_id,
            customer_name,
            created_at
        FROM bookings
        WHERE store_id = %s
          AND deleted_at IS NULL
        ORDER BY created_at DESC
        LIMIT 5
    """, (store_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows

# ============================================================
#   GET schedule BY STORE
# ============================================================
def get_schedule_from_bookings(store_id, date):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT 
            b.booking_id,
            TIME_FORMAT(b.booking_time, '%%H:%%i') AS booking_time,
            b.total_minutes,
            b.customer_name,
            IFNULL(e.fullname, 'ยังไม่กำหนด') AS employee_name
        FROM bookings b
        LEFT JOIN employee e ON b.employee_id = e.employee_id
        WHERE b.store_id = %s
          AND b.booking_date = %s
          AND b.deleted_at IS NULL
        ORDER BY b.booking_time ASC
    """, (store_id, date))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows



# ============================================================
#     ASSIGN EMPLOYEE TO BOOKING
# ============================================================
def get_schedule_by_date(store_id, date):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT 
            b.booking_id,
            b.booking_time,
            b.customer_name,
            e.fullname AS employee_name
        FROM bookings b
        LEFT JOIN employee e 
            ON b.employee_id = e.employee_id
        WHERE b.store_id = %s
          AND DATE(b.booking_date) = %s
          AND b.deleted_at IS NULL
        ORDER BY b.booking_time
    """

    cur.execute(sql, (store_id, date))
    rows = cur.fetchall()

    cur.close()
    conn.close()
    return rows


# ============================================================
#     CHECK EMPLOYEE TIME CONFLICT
# ============================================================
def check_employee_booking_conflict(employee_id, booking_date, booking_time):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT booking_id
        FROM bookings
        WHERE employee_id = %s
          AND booking_date = %s
          AND booking_time = %s
          AND deleted_at IS NULL
    """, (employee_id, booking_date, booking_time))

    result = cur.fetchone()

    cur.close()
    conn.close()

    return result is not None


# ============================================================
#     GET BOOKED TIMES BY EMPLOYEE
# ============================================================
def get_employee_booked_times(employee_id, booking_date):
    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT TIME_FORMAT(booking_time,'%%H:%%i') AS booking_time
        FROM bookings
        WHERE employee_id = %s
          AND booking_date = %s
          AND deleted_at IS NULL
    """, (employee_id, booking_date))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows

# ============================================================
#   GET BOOKED TIMES BY EMPLOYEE
# ============================================================
def get_employee_booked_times(employee_id, booking_date):

    conn = get_conn()
    cur = conn.cursor(pymysql.cursors.DictCursor)

    cur.execute("""
        SELECT TIME_FORMAT(booking_time,'%%H:%%i') AS booking_time
        FROM bookings
        WHERE employee_id = %s
          AND booking_date = %s
          AND deleted_at IS NULL
    """, (employee_id, booking_date))

    rows = cur.fetchall()

    cur.close()
    conn.close()

    return rows
