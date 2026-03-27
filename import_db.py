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

# 🔥 ใช้ตัวนี้เท่านั้น (ห้าม split)
for result in cursor.execute(sql, multi=True):
    pass

cursor.close()
conn.close()

print("✅ Import success")