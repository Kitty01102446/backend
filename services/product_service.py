from services.db import get_conn

def get_all_products():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_product_by_id(pid: int):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=%s", (pid,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row



def insert_product(name: str, price: float, image: str):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        INSERT INTO products (name, price, image)
        VALUES (%s, %s, %s)
    """
    cur.execute(sql, (name, price, image))
    new_id = cur.lastrowid

    cur.close()
    conn.close()
    return new_id



def update_product(pid: int, data: dict):
    conn = get_conn()
    cur = conn.cursor()

    sql = """
        UPDATE products
        SET name=%s, price=%s, image=%s
        WHERE id=%s
    """

    cur.execute(
        sql,
        (data.get("name"), data.get("price"), data.get("image", ""), pid)
    )

    conn.commit()
    updated = cur.rowcount > 0

    cur.close()
    conn.close()
    return updated


def delete_product(pid: int):
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("DELETE FROM products WHERE id=%s", (pid,))
    conn.commit()

    deleted = cur.rowcount > 0

    cur.close()
    conn.close()
    return deleted