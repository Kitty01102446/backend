"""
ผู้ดูแลระบบ (System Admin, role_id=4) -- ฟังก์ชันสำหรับหน้าแอดมินทั้งหมด:
แดชบอร์ด, จัดการร้าน (อนุมัติ/ปฏิเสธ/ประเมิน), จัดการผู้ใช้ (ดูกิจกรรม/แบน),
โปรไฟล์ลูกค้า, กิจกรรมทั้งหมด, สิทธิ์/บัญชี, รีวิว, การเงิน

ทุกฟังก์ชันในไฟล์นี้ถูกเรียกจาก endpoint ที่ผ่าน require_admin() แล้วเท่านั้น
(ดู backend/controllers/admin_controller.py)
"""

from services.db import get_conn


# ============================================================
#   DASHBOARD
# ============================================================
def get_dashboard_summary():
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) AS c FROM store WHERE deleted_at IS NULL")
    total_stores = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM store WHERE deleted_at IS NULL AND status_store_id = 4")
    pending_stores = cur.fetchone()["c"]

    cur.execute("SELECT COUNT(*) AS c FROM users WHERE deleted_at IS NULL")
    total_users = cur.fetchone()["c"]

    cur.execute("""
        SELECT COUNT(*) AS c FROM bookings
        WHERE deleted_at IS NULL AND booking_date = CURDATE()
    """)
    bookings_today = cur.fetchone()["c"]

    cur.execute("""
        SELECT COALESCE(SUM(total_price), 0) AS revenue FROM bookings
        WHERE deleted_at IS NULL AND status_booking_id = 3 AND booking_date = CURDATE()
    """)
    revenue_today = float(cur.fetchone()["revenue"])

    cur.execute("""
        SELECT COALESCE(SUM(total_price), 0) AS revenue FROM bookings
        WHERE deleted_at IS NULL AND status_booking_id = 3
          AND YEAR(booking_date) = YEAR(CURDATE()) AND MONTH(booking_date) = MONTH(CURDATE())
    """)
    revenue_month = float(cur.fetchone()["revenue"])

    cur.execute("""
        SELECT b.booking_id, b.booking_date, b.status_booking_id, sb.status_booking_name,
               s.store_name, b.customer_name
        FROM bookings b
        LEFT JOIN store s ON s.store_id = b.store_id
        LEFT JOIN status_booking sb ON sb.status_booking_id = b.status_booking_id
        WHERE b.deleted_at IS NULL
        ORDER BY b.booking_id DESC
        LIMIT 10
    """)
    recent_activity = cur.fetchall()

    cur.close()
    conn.close()
    return {
        "total_stores": total_stores,
        "pending_stores": pending_stores,
        "total_users": total_users,
        "bookings_today": bookings_today,
        "revenue_today": revenue_today,
        "revenue_month": revenue_month,
        "recent_activity": recent_activity,
    }


# ============================================================
#   STORE MANAGEMENT (approve / reject / evaluate)
# ============================================================
def get_stores_for_admin(status_store_id=None):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        SELECT
            s.store_id, s.store_name, s.phone, s.email, s.user_id,
            u.username AS owner_username,
            s.status_store_id, ss.status_store_name,
            s.admin_note, s.approved_by, s.approved_at, s.rejection_reason,
            s.created_at,
            (SELECT ROUND(AVG(rating), 2) FROM review WHERE store_id = s.store_id) AS avg_rating,
            (SELECT COUNT(*) FROM review WHERE store_id = s.store_id) AS review_count,
            (SELECT COUNT(*) FROM bookings WHERE store_id = s.store_id AND deleted_at IS NULL) AS booking_count
        FROM store s
        LEFT JOIN users u ON u.user_id = s.user_id
        LEFT JOIN status_store ss ON ss.status_store_id = s.status_store_id
        WHERE s.deleted_at IS NULL
    """
    params = []
    if status_store_id:
        sql += " AND s.status_store_id = %s"
        params.append(status_store_id)
    sql += " ORDER BY s.store_id DESC"

    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def approve_store(store_id: int, admin_user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE store
        SET status_store_id = 1, approved_by = %s, approved_at = NOW(),
            rejection_reason = NULL
        WHERE store_id = %s AND deleted_at IS NULL
    """, (admin_user_id, store_id))
    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated


def reject_store(store_id: int, admin_user_id: int, reason: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE store
        SET status_store_id = 5, approved_by = %s, approved_at = NOW(),
            rejection_reason = %s
        WHERE store_id = %s AND deleted_at IS NULL
    """, (admin_user_id, reason, store_id))
    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated


def set_store_admin_note(store_id: int, note: str):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE store SET admin_note = %s WHERE store_id = %s AND deleted_at IS NULL",
        (note, store_id)
    )
    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated


# ============================================================
#   USER MANAGEMENT (list / activity / ban)
# ============================================================
def get_users_for_admin():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            u.user_id, u.username, u.nickname, u.phone, u.email, u.role_id,
            r.role_name, u.is_banned, u.ban_reason, u.banned_at, u.created_at,
            (SELECT COUNT(*) FROM bookings WHERE user_id = u.user_id AND deleted_at IS NULL) AS booking_count
        FROM users u
        LEFT JOIN role r ON r.role_id = u.role_id
        WHERE u.deleted_at IS NULL
        ORDER BY u.user_id DESC
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def ban_user(user_id: int, reason: str, admin_user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET is_banned = 1, ban_reason = %s, banned_at = NOW(), banned_by = %s
        WHERE user_id = %s AND deleted_at IS NULL
    """, (reason, admin_user_id, user_id))
    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated


def unban_user(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE users
        SET is_banned = 0, ban_reason = NULL, banned_at = NULL, banned_by = NULL
        WHERE user_id = %s AND deleted_at IS NULL
    """, (user_id,))
    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated


# ============================================================
#   CUSTOMER PROFILE (admin view/edit)
# ============================================================
def get_user_profile_admin(user_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT user_id, username, nickname, phone, email, role_id, is_banned,
               ban_reason, created_at, updated_at
        FROM users
        WHERE user_id = %s AND deleted_at IS NULL
    """, (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    return user


def update_user_profile_admin(user_id: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    fields = []
    values = []
    for col in ("nickname", "phone", "email"):
        if col in data and data[col]:
            fields.append(f"{col}=%s")
            values.append(data[col])

    if not fields:
        cur.close()
        conn.close()
        return False

    values.append(user_id)
    cur.execute(
        f"UPDATE users SET {', '.join(fields)}, updated_at=NOW() WHERE user_id=%s AND deleted_at IS NULL",
        tuple(values)
    )
    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated


# ============================================================
#   ACTIVITY FEED (ทุกการจองทั้งแพลตฟอร์ม)
# ============================================================
def get_platform_activity(limit=200):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            b.booking_id,
            DATE_FORMAT(b.booking_date, '%%d/%%m/%%Y') AS booking_date,
            TIME_FORMAT(b.booking_time, '%%H:%%i') AS booking_time,
            b.customer_name,
            b.total_price,
            b.status_booking_id,
            sb.status_booking_name,
            s.store_id, s.store_name,
            e.fullname AS employee_name,
            GROUP_CONCAT(bs.service_name SEPARATOR ', ') AS services
        FROM bookings b
        LEFT JOIN store s ON s.store_id = b.store_id
        LEFT JOIN employee e ON e.employee_id = b.employee_id
        LEFT JOIN status_booking sb ON sb.status_booking_id = b.status_booking_id
        LEFT JOIN booking_services bs ON bs.booking_id = b.booking_id
        WHERE b.deleted_at IS NULL
        GROUP BY b.booking_id
        ORDER BY b.booking_id DESC
        LIMIT %s
    """, (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#   PERMISSIONS (role <-> permission assignment)
# ============================================================
def list_roles():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT role_id, role_name, description FROM role ORDER BY role_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def list_permissions():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT permission_id, code, name FROM permission ORDER BY permission_id")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def list_role_permissions():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT rp.role_permission_id, rp.role_id, r.role_name, rp.permission_id, p.code, p.name
        FROM role_permission rp
        JOIN role r ON r.role_id = rp.role_id
        JOIN permission p ON p.permission_id = rp.permission_id
        ORDER BY rp.role_id, rp.permission_id
    """)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def assign_permission(role_id: int, permission_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT role_permission_id FROM role_permission WHERE role_id=%s AND permission_id=%s",
        (role_id, permission_id)
    )
    if cur.fetchone():
        cur.close()
        conn.close()
        return None  # มีอยู่แล้ว

    cur.execute(
        "INSERT INTO role_permission (role_id, permission_id, created_at) VALUES (%s, %s, NOW())",
        (role_id, permission_id)
    )
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return new_id


def revoke_permission(role_permission_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM role_permission WHERE role_permission_id = %s", (role_permission_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    cur.close()
    conn.close()
    return deleted


# ============================================================
#   FINANCE (รายได้รวมแพลตฟอร์ม + แยกตามร้าน)
# ============================================================
def get_platform_finance(year: int, month: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT COALESCE(SUM(total_price), 0) AS total_revenue, COUNT(*) AS total_bookings
        FROM bookings
        WHERE deleted_at IS NULL AND status_booking_id = 3
          AND YEAR(booking_date) = %s AND MONTH(booking_date) = %s
    """, (year, month))
    totals = cur.fetchone()

    cur.execute("""
        SELECT
            s.store_id, s.store_name,
            COALESCE(SUM(b.total_price), 0) AS revenue,
            COUNT(b.booking_id) AS booking_count
        FROM store s
        LEFT JOIN bookings b
            ON b.store_id = s.store_id
           AND b.deleted_at IS NULL
           AND b.status_booking_id = 3
           AND YEAR(b.booking_date) = %s AND MONTH(b.booking_date) = %s
        WHERE s.deleted_at IS NULL
        GROUP BY s.store_id, s.store_name
        ORDER BY revenue DESC
    """, (year, month))
    by_store = cur.fetchall()

    cur.close()
    conn.close()
    return {
        "total_revenue": float(totals["total_revenue"]),
        "total_bookings": totals["total_bookings"],
        "by_store": by_store,
    }


# ============================================================
#   REVIEW MODERATION
# ============================================================
def list_reviews_for_admin(only_hidden=False):
    conn = get_conn()
    cur = conn.cursor()
    sql = """
        SELECT
            rv.review_id, rv.rating, rv.comment, rv.is_hidden, rv.hidden_reason,
            rv.created_at, rv.user_id, u.username,
            rv.store_id, s.store_name
        FROM review rv
        LEFT JOIN users u ON u.user_id = rv.user_id
        LEFT JOIN store s ON s.store_id = rv.store_id
    """
    if only_hidden:
        sql += " WHERE rv.is_hidden = 1"
    sql += " ORDER BY rv.review_id DESC"

    cur.execute(sql)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def set_review_hidden(review_id: int, hidden: bool, reason: str = None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "UPDATE review SET is_hidden = %s, hidden_reason = %s WHERE review_id = %s",
        (1 if hidden else 0, reason if hidden else None, review_id)
    )
    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated
