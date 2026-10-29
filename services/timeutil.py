"""
ยูทิลิตี้เวลา - ใช้เวลาโซน Asia/Bangkok เป็นมาตรฐานเดียวของระบบ

ห้ามใช้ NOW()/CURDATE() ของ MySQL ในการเปรียบเทียบ business logic เพราะ
session timezone ของ DB ไม่ได้ถูกตั้งค่าไว้ ให้คำนวณ "วันนี้"/"ตอนนี้" ที่ฝั่ง
Python ด้วยไฟล์นี้เสมอ
"""

from datetime import datetime, date, time
from zoneinfo import ZoneInfo

BANGKOK_TZ = ZoneInfo("Asia/Bangkok")


def bangkok_now() -> datetime:
    return datetime.now(BANGKOK_TZ)


def bangkok_today() -> date:
    return bangkok_now().date()


def bangkok_time_now() -> time:
    return bangkok_now().time()


def combine_bkk(date_val, time_val) -> datetime:
    """รวมค่า date + time (ที่มาจาก DB) ให้เป็น datetime แบบ aware ในโซน Bangkok"""
    return datetime.combine(date_val, time_val, tzinfo=BANGKOK_TZ)


def to_date(value) -> date:
    """แปลงค่าที่อาจเป็น str (จาก JSON/query string เช่น "2026-04-01") หรือ
    date object (จากแถวที่อ่านจาก DB) ให้เป็น date object เสมอ"""
    if isinstance(value, date):
        return value
    return date.fromisoformat(str(value)[:10])


def iso_day_of_week(date_val) -> int:
    """1=Monday .. 7=Sunday, ตรงกับ date.isoweekday()"""
    return to_date(date_val).isoweekday()
