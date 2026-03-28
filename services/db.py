"""
ส่วนจัดการการเชื่อมต่อฐานข้อมูล (DB)

ฟังก์ชันที่นี่จะคืน connection ใหม่ทุกครั้งที่เรียก เพื่อให้แต่ละคำขอสามารถแยกการเชื่อมต่อได้
ค่า config จะอ่านจาก environment variables (เช่น .env)
คอมเมนต์ทั้งหมดเป็นภาษาไทยตามคำขอ
"""

import os
import pymysql
from pymysql.cursors import DictCursor
from urllib.parse import urlparse, unquote


def _get_env(*keys, default=None):
    """คืนค่า env ตัวแรกที่มีข้อมูล เพื่อรองรับหลายชื่อ key"""
    for key in keys:
        value = os.getenv(key)
        if value not in (None, ""):
            return value
    return default


def _parse_db_url():
    """แปลงค่า connection URL ให้เป็นส่วนประกอบสำหรับ pymysql"""
    raw_url = _get_env("DB_URL", "DATABASE_URL", "MYSQL_URL", "MYSQL_PUBLIC_URL")
    if not raw_url:
        return {}

    parsed = urlparse(raw_url)
    if parsed.scheme not in {"mysql", "mysql2"}:
        return {}

    db_name = parsed.path.lstrip("/") or None
    return {
        "host": parsed.hostname,
        "port": parsed.port,
        "user": unquote(parsed.username) if parsed.username else None,
        "password": unquote(parsed.password) if parsed.password else None,
        "database": unquote(db_name) if db_name else None,
    }


def _get_db_config():
    """เตรียม dictionary ของการตั้งค่า DB โดยอ่านจาก environment variables

    ค่าพื้นฐานจะถูกใช้เป็นค่าเริ่มต้นถ้าไม่ได้กำหนดใน env
    """
    url_config = _parse_db_url()
    port_value = _get_env("DB_PORT", "MYSQLPORT", default=str(url_config.get("port") or "3306"))
    host_value = _get_env("DB_HOST", "MYSQLHOST", default=url_config.get("host"))
    user_value = _get_env("DB_USER", "MYSQLUSER", default=url_config.get("user"))
    password_value = _get_env("DB_PASS", "MYSQLPASSWORD", default=url_config.get("password"))
    database_value = _get_env("DB_NAME", "MYSQLDATABASE", default=url_config.get("database"))

    config = {
        "host": host_value,
        "port": int(port_value),
        "user": user_value,
        "password": password_value,
        "database": database_value,
        "cursorclass": DictCursor,
        "charset": "utf8mb4",
        "autocommit": True,
        "connect_timeout": 10,
        "read_timeout": 30,
        "write_timeout": 30,
    }

    use_ssl_value = _get_env("DB_SSL", "MYSQL_SSL", default="true")
    use_ssl = str(use_ssl_value).lower() not in {"0", "false", "no"}
    if host_value and host_value not in {"127.0.0.1", "localhost"} and use_ssl:
        # รองรับ managed MySQL ที่อยู่หลัง proxy/public endpoint
        config["ssl"] = {}

    return config


def get_conn():
    """สร้างและคืนค่าการเชื่อมต่อฐานข้อมูลใหม่

    ผู้เรียกต้องรับผิดชอบในการปิด cursor และ connection เมื่อเสร็จ
    """
    return pymysql.connect(**_get_db_config())
