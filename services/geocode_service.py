"""
แปลงที่อยู่ร้าน (ข้อความ) เป็นพิกัด latitude/longitude อัตโนมัติ
ใช้ Nominatim (OpenStreetMap) เพราะเป็นบริการฟรี ไม่ต้องขอ API Key

หมายเหตุ: เป็น best-effort เท่านั้น -- ถ้า geocode ไม่สำเร็จ (เช่น ที่อยู่ไม่ครบ,
network error, หา location ไม่เจอ) จะคืนค่า (None, None) เสมอ ไม่ raise exception
เพื่อไม่ให้การสมัครร้าน/แก้ไขที่อยู่ล้มเหลวเพราะ geocoding
"""

import requests

NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
USER_AGENT = "GlamNailApp/1.0 (contact: chakrit.u@kkumail.com)"


def geocode_address(address_text: str):
    """คืนค่า (latitude, longitude) หรือ (None, None) ถ้า geocode ไม่สำเร็จ"""
    if not address_text or not address_text.strip():
        return None, None

    try:
        resp = requests.get(
            NOMINATIM_URL,
            params={
                "q": address_text,
                "format": "json",
                "limit": 1,
                "countrycodes": "th",
            },
            headers={"User-Agent": USER_AGENT},
            timeout=5,
        )
        resp.raise_for_status()
        results = resp.json()
        if results:
            return float(results[0]["lat"]), float(results[0]["lon"])
    except Exception as e:
        print(f"[geocode_service] geocoding failed for '{address_text}': {e!r}")

    return None, None
