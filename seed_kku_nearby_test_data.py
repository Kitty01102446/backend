"""
=====================================================================
  SEED / TEST DATA -- DEVELOPMENT ONLY, NOT REAL SHOP DATA
=====================================================================
สคริปต์นี้เพิ่มร้านทำเล็บตัวอย่าง 7 ร้าน กระจายรอบมหาวิทยาลัยขอนแก่น (มข.)
สำหรับทดสอบฟีเจอร์ "ร้านใกล้ฉัน" (GET /store/nearby) โดยเฉพาะ

- ใช้ตาราง store / store_address / employee / review / click_log / bookings
  ที่มีอยู่แล้วในระบบ ไม่มีการสร้างตารางใหม่
- พิกัด latitude/longitude ไม่ได้สุ่มขึ้นมาเอง แต่ได้จากการเรียก
  services/geocode_service.py (Nominatim/OpenStreetMap) ผ่านฟังก์ชัน
  insert_store_address() ตัวเดียวกับที่ระบบสมัครร้านค้าจริงใช้อยู่แล้ว
- ทุกร้านตั้งชื่อขึ้นต้นด้วย "[SEED-TEST]" เพื่อไม่ให้สับสนกับร้านจริง
  และสามารถลบออกได้ทั้งหมดด้วยสคริปต์ cleanup ท้ายไฟล์นี้ (ดู __main__)

รัน:  python seed_kku_nearby_test_data.py
ลบ:   python seed_kku_nearby_test_data.py --cleanup
"""

import sys
from dotenv import load_dotenv

load_dotenv()

from services.db import get_conn
from services.store_address_service import insert_store_address
from services.employee_service import insert_employee
from services.review_service import insert_review
from services.click_log_service import insert_click_log

SEED_TAG = "[SEED-TEST]"

# เจ้าของร้าน (owner) ใช้ user_id ที่มีอยู่แล้วในระบบ (users_controller ใช้ user_id นี้ตอนสมัครร้านจริง)
OWNER_USER_ID = 1
# user_id ที่ใช้แนบกับ review / click_log (หมุนใช้ผู้ใช้ที่มีอยู่จริงในตาราง users)
REVIEWER_USER_IDS = [1, 2, 3, 4, 5]

# ---------------------------------------------------------------
# ร้านทดสอบ 7 ร้าน กระจายระยะจาก มข. -- ระยะทางคำนวณจริงหลัง geocode
# (ดูสรุประยะทางท้ายการรัน)
#   ที่อยู่ (street/subdistrict/district/province) ผ่านการทดสอบแล้วว่า
#   geocode_service หาพิกัดได้จริงและตรงพื้นที่ (ดู session ที่ยืนยันไว้)
# ---------------------------------------------------------------
STORES = [
    {
        "store_name": f"{SEED_TAG} เล็บสวย มข. Nail Studio",
        "price": 250,
        "phone": "0810000001",
        "email": "seed.kku.campus@example.test",
        "image": "kku_engineer.jpg",
        "status_store_id": 1,  # active
        "address": {
            "street": "มหาวิทยาลัยขอนแก่น",
            "subdistrict": "ในเมือง",
            "district": "เมืองขอนแก่น",
            "province": "ขอนแก่น",
            "postal_code": "40002",
        },
        "open_time": "00:00:00",
        "close_time": "23:59:00",  # เปิด 24 ชม. -> ใช้ทดสอบ is_open = True
        "recommend_text": "ข้อมูลทดสอบ (Seed/Test Data) — ร้านในรั้ว มข. ใกล้ที่สุด สำหรับทดสอบ Sort ตามระยะทาง",
        "employees": ["ช่างมด", "ช่างแนน", "ช่างพลอย", "ช่างกิ๊ฟ"],
        "ratings": [5, 5, 4],
        "clicks": 5,
        "bookings_today": 1,  # จำนวนคิวที่จองวันนี้ (ลด available_slots)
    },
    {
        "store_name": f"{SEED_TAG} เซ็นทรัลขอนแก่น เนล บาร์",
        "price": 350,
        "phone": "0810000002",
        "email": "seed.central.kk@example.test",
        "image": "kk_central.jpg",
        "status_store_id": 1,
        "address": {
            "street": "เซ็นทรัลขอนแก่น",
            "subdistrict": "ในเมือง",
            "district": "เมืองขอนแก่น",
            "province": "ขอนแก่น",
            "postal_code": "40000",
        },
        "open_time": "10:00:00",
        "close_time": "20:00:00",  # ช่วงเวลาปกติ -> อาจ is_open = False นอกเวลาทำการ
        "recommend_text": "ข้อมูลทดสอบ (Seed/Test Data) — ใกล้ มข. ประมาณ 2 กม.",
        "employees": ["ช่างเบล", "ช่างฟ้า", "ช่างนุ่น"],
        "ratings": [4, 4, 3],
        "clicks": 3,
        "bookings_today": 0,
    },
    {
        "store_name": f"{SEED_TAG} ศิลา เนล เลาจน์",
        "price": 300,
        "phone": "0810000003",
        "email": "seed.sila@example.test",
        "image": "",
        "status_store_id": 1,
        "address": {
            "street": "ถนนกัลปพฤกษ์",
            "subdistrict": "ศิลา",
            "district": "เมืองขอนแก่น",
            "province": "ขอนแก่น",
            "postal_code": "40000",
        },
        "open_time": "00:00:00",
        "close_time": "23:59:00",  # is_open = True
        "recommend_text": "ข้อมูลทดสอบ (Seed/Test Data) — ตำบลศิลา ใกล้ มข. ประมาณ 2 กม.",
        "employees": ["ช่างมิ้นท์", "ช่างเมย์"],
        "ratings": [5, 4, 5, 5],
        "clicks": 8,
        "bookings_today": 1,
    },
    {
        "store_name": f"{SEED_TAG} มิตรภาพ-บ้านเป็ด เนล",
        "price": 280,
        "phone": "0810000004",
        "email": "seed.banphet@example.test",
        "image": "",
        "status_store_id": 2,  # closed -> ใช้ทดสอบ is_open = False (จาก status ไม่ใช่เวลา)
        "address": {
            "street": "ถนนมิตรภาพ",
            "subdistrict": "บ้านเป็ด",
            "district": "เมืองขอนแก่น",
            "province": "ขอนแก่น",
            "postal_code": "40000",
        },
        "open_time": "09:00:00",
        "close_time": "21:00:00",
        "recommend_text": "ข้อมูลทดสอบ (Seed/Test Data) — ถนนมิตรภาพ ใกล้ มข. ประมาณ 2.8 กม. (ปิดปรับปรุงชั่วคราว)",
        "employees": ["ช่างแป้ง", "ช่างต้น"],
        "ratings": [3, 3],
        "clicks": 1,
        "bookings_today": 0,
    },
    {
        "store_name": f"{SEED_TAG} ทุ่งสร้าง เนล สตูดิโอ",
        "price": 320,
        "phone": "0810000005",
        "email": "seed.thungsang@example.test",
        "image": "",
        "status_store_id": 1,
        "address": {
            "street": "ทุ่งสร้าง",
            "subdistrict": "ในเมือง",
            "district": "เมืองขอนแก่น",
            "province": "ขอนแก่น",
            "postal_code": "40000",
        },
        "open_time": "10:00:00",
        "close_time": "20:00:00",
        "recommend_text": "ข้อมูลทดสอบ (Seed/Test Data) — ห่างจาก มข. เล็กน้อย ประมาณ 4.3 กม.",
        "employees": ["ช่างข้าวปุ้น", "ช่างส้ม", "ช่างเจน", "ช่างวุ้น", "ช่างปุ๊ก"],
        "ratings": [4, 5],
        "clicks": 4,
        "bookings_today": 2,
    },
    {
        "store_name": f"{SEED_TAG} น้ำพอง เนล เฮาส์",
        "price": 220,
        "phone": "0810000006",
        "email": "seed.namphong@example.test",
        "image": "",
        "status_store_id": 1,
        "address": {
            "street": "ถนนมิตรภาพ",
            "subdistrict": "น้ำพอง",
            "district": "น้ำพอง",
            "province": "ขอนแก่น",
            "postal_code": "40140",
        },
        "open_time": "00:00:00",
        "close_time": "23:59:00",  # is_open = True
        "recommend_text": "ข้อมูลทดสอบ (Seed/Test Data) — อยู่ไกลจาก มข. ประมาณ 16 กม. (ทดสอบการกรองตามรัศมี)",
        "employees": ["ช่างแมว"],
        "ratings": [5],
        "clicks": 2,
        "bookings_today": 1,  # 1 ช่าง จอง 1 คิว -> available_slots = 0
    },
    {
        "store_name": f"{SEED_TAG} บ้านฝาง เนล ช็อป",
        "price": 200,
        "phone": "0810000007",
        "email": "seed.banfang@example.test",
        "image": "",
        "status_store_id": 1,
        "address": {
            "street": "",
            "subdistrict": "",
            "district": "บ้านฝาง",
            "province": "ขอนแก่น",
            "postal_code": "40270",
        },
        "open_time": "10:00:00",
        "close_time": "20:00:00",
        "recommend_text": "ข้อมูลทดสอบ (Seed/Test Data) — อยู่ไกลจาก มข. มากที่สุดในชุดทดสอบนี้ ประมาณ 24 กม.",
        "employees": ["ช่างนิด", "ช่างหนึ่ง", "ช่างสอง"],
        "ratings": [2, 3],
        "clicks": 1,
        "bookings_today": 0,
    },
]


def seed():
    conn = get_conn()
    cur = conn.cursor()

    created_store_ids = []

    for i, s in enumerate(STORES):
        # 1) STORE
        cur.execute(
            """
            INSERT INTO store (store_name, price, phone, email, user_id, image, status_store_id, created_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s, NOW())
            """,
            (
                s["store_name"], s["price"], s["phone"], s["email"],
                OWNER_USER_ID, s["image"], s["status_store_id"],
            ),
        )
        store_id = cur.lastrowid
        conn.commit()
        created_store_ids.append(store_id)

        # 2) STORE_ADDRESS -- ใช้ insert_store_address() ตัวเดียวกับระบบจริง
        #    ฟังก์ชันนี้ auto-geocode ที่อยู่ -> latitude/longitude ให้เอง
        addr = dict(s["address"])
        addr["store_id"] = store_id
        addr["is_verified"] = 1
        addr["has_parking"] = 0
        addr["open_time"] = s["open_time"]
        addr["close_time"] = s["close_time"]
        addr["recommend_text"] = s["recommend_text"]
        store_address_id = insert_store_address(addr)

        # 3) EMPLOYEES
        for name in s["employees"]:
            insert_employee(name, "080" + str(1000000 + store_id), "", "Nail Artist", store_id)

        # 4) REVIEWS
        for j, rating in enumerate(s["ratings"]):
            reviewer = REVIEWER_USER_IDS[j % len(REVIEWER_USER_IDS)]
            insert_review(rating, f"{SEED_TAG} รีวิวทดสอบ", reviewer, store_id)

        # 5) CLICK_LOG (popularity signal ที่ /store/nearby ใช้จริง)
        for k in range(s["clicks"]):
            reviewer = REVIEWER_USER_IDS[k % len(REVIEWER_USER_IDS)]
            insert_click_log(reviewer, store_id)

        # 6) BOOKINGS วันนี้ (ลด available_slots ตามที่ get_nearby_stores คำนวณ)
        for b in range(s["bookings_today"]):
            reviewer = REVIEWER_USER_IDS[b % len(REVIEWER_USER_IDS)]
            cur.execute(
                """
                INSERT INTO bookings (
                    user_id, store_id, employee_id, booking_date, booking_time,
                    customer_name, customer_phone, total_price, total_minutes,
                    status_booking_id, type_booking_id, created_at
                ) VALUES (%s, %s, NULL, CURDATE(), '12:00:00', %s, '0800000000', %s, 60, 2, 1, NOW())
                """,
                (reviewer, store_id, f"{SEED_TAG} ลูกค้าทดสอบ", s["price"]),
            )
        conn.commit()

        print(f"  ✓ store_id={store_id:<4} store_address_id={store_address_id:<4} {s['store_name']}")

    cur.close()
    conn.close()
    return created_store_ids


def cleanup():
    """ลบข้อมูลทดสอบทั้งหมดที่ชื่อร้านขึ้นต้นด้วย SEED_TAG (สำหรับ dev เท่านั้น)"""
    conn = get_conn()
    cur = conn.cursor()

    cur.execute("SELECT store_id FROM store WHERE store_name LIKE %s", (f"{SEED_TAG}%",))
    ids = [r["store_id"] for r in cur.fetchall()]

    if not ids:
        print("ไม่พบข้อมูล seed ที่ต้องลบ")
        cur.close()
        conn.close()
        return

    fmt_ids = ",".join(str(i) for i in ids)
    for table in ["bookings", "review", "click_log", "employee", "store_address"]:
        cur.execute(f"DELETE FROM {table} WHERE store_id IN ({fmt_ids})")
    cur.execute(f"DELETE FROM store WHERE store_id IN ({fmt_ids})")
    conn.commit()
    cur.close()
    conn.close()
    print(f"ลบร้านทดสอบ {len(ids)} ร้านเรียบร้อย: {ids}")


if __name__ == "__main__":
    if "--cleanup" in sys.argv:
        cleanup()
    else:
        print(f"กำลังเพิ่มร้านทดสอบ {len(STORES)} ร้านรอบมหาวิทยาลัยขอนแก่น...")
        ids = seed()
        print(f"เสร็จสิ้น -- เพิ่มร้านทดสอบทั้งหมด {len(ids)} ร้าน: {ids}")
