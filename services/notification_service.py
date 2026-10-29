"""
ระบบแจ้งเตือน (Notification) ใช้ร่วมกันทั้งฝั่งลูกค้าและฝั่งร้าน

recipient_user_id คือ users.user_id เสมอ ไม่ว่าผู้รับจะเป็นลูกค้า (role_id=1)
หรือเจ้าของร้าน (role_id=2, ผ่าน store.user_id) จึงไม่ต้องมีตาราง "ประเภทผู้รับ" แยก
"""

from services.db import get_conn


# ============================================================
#                      CREATE NOTIFICATION
# ============================================================
def create_notification(recipient_user_id: int, booking_id, type_: str, title: str, message: str):
    if not recipient_user_id:
        return None

    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO notification
            (recipient_user_id, booking_id, type, title, message, is_read, created_at)
        VALUES (%s, %s, %s, %s, %s, 0, NOW())
    """, (recipient_user_id, booking_id, type_, title, message))

    new_id = cur.lastrowid
    conn.commit()
    cur.close()
    conn.close()
    return new_id


# ============================================================
#              GET NOTIFICATIONS FOR A USER (ล่าสุดก่อน)
# ============================================================
def get_notifications(user_id: int, limit: int = 50):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            notification_id, recipient_user_id, booking_id,
            type, title, message, is_read, created_at
        FROM notification
        WHERE recipient_user_id = %s
        ORDER BY created_at DESC
        LIMIT %s
    """, (user_id, limit))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


# ============================================================
#                     GET UNREAD COUNT
# ============================================================
def get_unread_count(user_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT COUNT(*) AS unread_count
        FROM notification
        WHERE recipient_user_id = %s AND is_read = 0
    """, (user_id,))

    row = cur.fetchone()
    cur.close()
    conn.close()
    return row["unread_count"] if row else 0


# ============================================================
#                MARK ONE NOTIFICATION AS READ
# ============================================================
def mark_read(notification_id: int, user_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE notification
        SET is_read = 1
        WHERE notification_id = %s AND recipient_user_id = %s
    """, (notification_id, user_id))

    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated


# ============================================================
#                MARK ALL NOTIFICATIONS AS READ
# ============================================================
def mark_all_read(user_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        UPDATE notification
        SET is_read = 1
        WHERE recipient_user_id = %s AND is_read = 0
    """, (user_id,))

    conn.commit()
    updated_count = cur.rowcount
    cur.close()
    conn.close()
    return updated_count
