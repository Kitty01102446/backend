import pymysql
import os

conn = pymysql.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT")),
    autocommit=True
)

cursor = conn.cursor()

with open("nailshop.sql", "r", encoding="utf-8") as f:
    sql = f.read()

# 🔥 แยกคำสั่ง SQL ทีละตัว
statements = [s.strip() for s in sql.split(";") if s.strip()]

for stmt in statements:
    try:
        cursor.execute(stmt)
    except Exception as e:
        print("⚠️ Skip:", e)

cursor.close()
conn.close()

print("✅ Import done")