"""
ข้อร้องเรียนระหว่างลูกค้ากับร้านค้า -- ลูกค้า/เจ้าของร้านแจ้งเรื่องเข้ามา,
ผู้ดูแลระบบ (role_id=4) เป็นคนตัดสิน/ปิดเรื่อง
"""

from services.db import get_conn


def create_complaint(reporter_user_id: int, subject: str, detail: str,
                      booking_id=None, against_store_id=None):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO complaint
            (booking_id, reporter_user_id, against_store_id, subject, detail, status)
        VALUES (%s, %s, %s, %s, %s, 'OPEN')
    """, (booking_id, reporter_user_id, against_store_id, subject, detail))
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return new_id


def list_complaints(status=None):
    conn = get_conn()
    cur = conn.cursor()
    sql = """
        SELECT
            c.complaint_id, c.booking_id, c.subject, c.detail, c.status,
            c.resolution_note, c.resolved_by, c.resolved_at, c.created_at,
            c.reporter_user_id, u.username AS reporter_username,
            c.against_store_id, s.store_name
        FROM complaint c
        LEFT JOIN users u ON u.user_id = c.reporter_user_id
        LEFT JOIN store s ON s.store_id = c.against_store_id
    """
    params = []
    if status:
        sql += " WHERE c.status = %s"
        params.append(status)
    sql += " ORDER BY c.complaint_id DESC"

    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_complaint_by_id(complaint_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        SELECT
            c.complaint_id, c.booking_id, c.subject, c.detail, c.status,
            c.resolution_note, c.resolved_by, c.resolved_at, c.created_at,
            c.reporter_user_id, u.username AS reporter_username,
            c.against_store_id, s.store_name
        FROM complaint c
        LEFT JOIN users u ON u.user_id = c.reporter_user_id
        LEFT JOIN store s ON s.store_id = c.against_store_id
        WHERE c.complaint_id = %s
    """, (complaint_id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


def resolve_complaint(complaint_id: int, status: str, resolution_note: str, resolved_by: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        UPDATE complaint
        SET status = %s, resolution_note = %s, resolved_by = %s, resolved_at = NOW()
        WHERE complaint_id = %s
    """, (status, resolution_note, resolved_by, complaint_id))
    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated
