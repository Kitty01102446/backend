from services.db import get_conn

# ============================================================
#                SELECT ALL CLICK_LOG
# ============================================================
def get_all_click_logs():
    conn = get_conn()
    cur = conn.cursor()
    # ใช้ SELECT เฉพาะคอลัมน์ที่ต้องการ และใช้ AS เพื่อเปลี่ยนชื่อคอลัมน์ที่ไม่ซ้ำกัน
    cur.execute("""
      SELECT 
    click_log.click_log_id, 
    click_log.user_id AS click_log_user_id, 
    click_log.store_id AS click_log_store_id, 
    click_log.created_at, 
    click_log.updated_at, 
    click_log.deleted_at, 

    store.store_id,
    store.store_name,
    store.price,
    store.image,

    users.user_id,
    review.rating,

    GROUP_CONCAT(tag.tag_name) AS tag   -- ✅ tag ร้าน

FROM click_log
JOIN store ON click_log.store_id = store.store_id
JOIN users ON click_log.user_id = users.user_id

LEFT JOIN review 
  ON click_log.store_id = review.store_id 
 AND click_log.user_id = review.user_id

LEFT JOIN store_tag ON store.store_id = store_tag.store_id
LEFT JOIN tag ON store_tag.tag_id = tag.tag_id

WHERE click_log.deleted_at IS NULL
GROUP BY click_log.click_log_id;

    """)
    rows = cur.fetchall()  # ดึงข้อมูลทั้งหมด
    columns = [col_desc[0] for col_desc in cur.description]  # เก็บชื่อคอลัมน์ทั้งหมด
    cur.close()
    conn.close()

    # ตรวจสอบชื่อคอลัมน์ที่ดึงมา
    print(columns)  # ดูชื่อคอลัมน์ที่ดึงมา

    # แปลงข้อมูลแต่ละแถวให้เป็น dictionary โดยใช้ชื่อคอลัมน์ที่ถูกต้อง
    results = []
    for row in rows:
        row_dict = dict(zip(columns, row))
        print(row_dict)  # ดูค่าที่แปลงแล้ว
        results.append(row_dict)

    return rows

# ============================================================
#                SELECT CLICK_LOG BY ID
# ============================================================
def get_click_log_by_id(cid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM click_log WHERE click_log_id=%s", (cid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row


# ============================================================
#                INSERT CLICK_LOG
# ============================================================
def insert_click_log(user_id: int, store_id: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO click_log (user_id, store_id, created_at)
        VALUES (%s, %s, NOW())
    """

    cur.execute(sql, (user_id, store_id))
    new_id = cur.lastrowid
    conn.commit()

    cur.close()
    conn.close()
    return new_id


# ============================================================
#                UPDATE CLICK_LOG
# ============================================================
def update_click_log(cid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE click_log
        SET user_id=%s,
            store_id=%s,
            updated_at = NOW()
        WHERE click_log_id=%s
    """

    cur.execute(sql, (
        data.get("user_id"),
        data.get("store_id"),
        cid
    ))

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


# ============================================================
#                DELETE CLICK_LOG
# ============================================================
def delete_click_log(cid: int):
    conn = get_conn()
    cur = conn.cursor()

    sql = "Update  address set deleted_at = now() where address_id=%s"

    cur.execute("DELETE FROM click_log WHERE click_log_id=%s", (cid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted
