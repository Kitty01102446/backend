"""
ส่วนจัดการการเชื่อมต่อฐานข้อมูล (DB)

ฟังก์ชันที่นี่จะคืน connection ใหม่ทุกครั้งที่เรียก เพื่อให้แต่ละคำขอสามารถแยกการเชื่อมต่อได้
ค่า config จะอ่านจาก environment variables (เช่น .env)
คอมเมนต์ทั้งหมดเป็นภาษาไทยตามคำขอ
"""

import os
import pymysql
from pymysql.cursors import DictCursor


def _get_env(*keys, default=None):
    """คืนค่า env ตัวแรกที่มีข้อมูล เพื่อรองรับหลายชื่อ key"""
    for key in keys:
        value = os.getenv(key)
        if value not in (None, ""):
            return value
    return default


def _get_db_config():
    """เตรียม dictionary ของการตั้งค่า DB โดยอ่านจาก environment variables

    ค่าพื้นฐานจะถูกใช้เป็นค่าเริ่มต้นถ้าไม่ได้กำหนดใน env
    """
    port_value = _get_env("DB_PORT", "MYSQLPORT", default="3306")

    return {
        "host": _get_env("DB_HOST", "MYSQLHOST"),
        "port": int(port_value),
        "user": _get_env("DB_USER", "MYSQLUSER"),
        "password": _get_env("DB_PASS", "MYSQLPASSWORD"),
        "database": _get_env("DB_NAME", "MYSQLDATABASE"),
        "cursorclass": DictCursor,
        "charset": "utf8mb4",
        "autocommit": True,
    }


def get_conn():
    """สร้างและคืนค่าการเชื่อมต่อฐานข้อมูลใหม่

    ผู้เรียกต้องรับผิดชอบในการปิด cursor และ connection เมื่อเสร็จ
    """
    return pymysql.connect(**_get_db_config())
