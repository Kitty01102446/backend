import pymysql
import os

conn = pymysql.connect(
    host=os.getenv("MYSQLHOST"),
    user=os.getenv("MYSQLUSER"),
    password=os.getenv("MYSQLPASSWORD"),
    database=os.getenv("MYSQLDATABASE"),
    port=int(os.getenv("MYSQLPORT"))
)

cursor = conn.cursor()

with open("nailshop.sql", "r", encoding="utf-8") as f:
    sql = f.read()

for statement in sql.split(";"):
    if statement.strip():
        cursor.execute(statement)

conn.commit()
conn.close()

print("✅ Import success")