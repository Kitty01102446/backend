"""
ทักษะพนักงานต่อบริการ (employee_service_skill)

ผูกพนักงานกับบริการที่ทำได้แบบรายตัว (ไม่ใช่รายหมวดหมู่)
"""

from services.db import get_conn


# ============================================================
#   GET SKILLS BY EMPLOYEE
# ============================================================
def get_employee_skills(employee_id: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("""
        SELECT service_id
        FROM employee_service_skill
        WHERE employee_id = %s
    """, (employee_id,))

    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [r["service_id"] for r in rows]


# ============================================================
#   SET SKILLS BY EMPLOYEE (REPLACE-ALL)
# ============================================================
def set_employee_skills(employee_id: int, service_ids: list):
    conn = get_conn()
    cur = conn.cursor()

    try:
        conn.begin()

        cur.execute("DELETE FROM employee_service_skill WHERE employee_id = %s", (employee_id,))

        service_ids = [sid for sid in (service_ids or []) if sid is not None]
        if service_ids:
            cur.executemany(
                "INSERT INTO employee_service_skill (employee_id, service_id) VALUES (%s, %s)",
                [(employee_id, sid) for sid in service_ids]
            )

        conn.commit()
        return True

    except Exception:
        conn.rollback()
        raise

    finally:
        cur.close()
        conn.close()
