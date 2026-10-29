"""
เนื้อหาหน้าเว็บ (แบนเนอร์/ข่าวสาร/ประกาศ) ที่ผู้ดูแลระบบจัดการได้
"""

from services.db import get_conn


def list_content(content_type=None, only_active=False):
    conn = get_conn()
    cur = conn.cursor()
    sql = "SELECT * FROM site_content WHERE 1=1"
    params = []
    if content_type:
        sql += " AND content_type = %s"
        params.append(content_type)
    if only_active:
        sql += " AND is_active = 1"
    sql += " ORDER BY display_order ASC, content_id DESC"

    cur.execute(sql, tuple(params))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def create_content(data: dict, created_by: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO site_content
            (content_type, title, body, image_url, link_url, display_order, is_active, created_by)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data.get("content_type"),
        data.get("title"),
        data.get("body"),
        data.get("image_url"),
        data.get("link_url"),
        data.get("display_order", 0),
        1 if data.get("is_active", True) else 0,
        created_by,
    ))
    conn.commit()
    new_id = cur.lastrowid
    cur.close()
    conn.close()
    return new_id


def update_content(content_id: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    fields = []
    values = []
    for col in ("content_type", "title", "body", "image_url", "link_url", "display_order"):
        if col in data:
            fields.append(f"{col}=%s")
            values.append(data[col])
    if "is_active" in data:
        fields.append("is_active=%s")
        values.append(1 if data["is_active"] else 0)

    if not fields:
        cur.close()
        conn.close()
        return False

    values.append(content_id)
    cur.execute(
        f"UPDATE site_content SET {', '.join(fields)}, updated_at=NOW() WHERE content_id=%s",
        tuple(values)
    )
    conn.commit()
    updated = cur.rowcount > 0
    cur.close()
    conn.close()
    return updated


def delete_content(content_id: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("DELETE FROM site_content WHERE content_id = %s", (content_id,))
    conn.commit()
    deleted = cur.rowcount > 0
    cur.close()
    conn.close()
    return deleted
