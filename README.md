# Backend

Flask backend สำหรับ deploy บน Railway โดยเชื่อมต่อ MySQL ผ่าน environment variables

## Deploy บน Railway

1. Push repo นี้ขึ้น GitHub
2. ใน Railway กด `New Project`
3. เลือก `Deploy from GitHub repo`
4. เลือก repo นี้
5. Railway จะ build จาก [Dockerfile](/Users/kitty/Desktop/C/backend/Dockerfile) อัตโนมัติ

## Environment Variables ที่ต้องตั้ง

ตั้งค่าใน Railway ตามนี้

```env
DB_HOST=your-mysql-host
DB_PORT=3306
DB_USER=your-mysql-user
DB_PASS=your-mysql-password
DB_NAME=your-mysql-database
PORT=5000
```

หมายเหตุ:
- ถ้าใช้ MySQL ของ Railway เอง ให้คัดลอกค่าจาก service database มาใส่
- ไฟล์ `.env` ในเครื่องใช้สำหรับ local development เท่านั้น Railway จะใช้ค่าจากหน้า Variables

## Start Command

ถ้า Railway ถาม start command หรือไม่ได้ใช้ Dockerfile ให้ใช้:

```bash
gunicorn -b 0.0.0.0:$PORT app:app
```

## Dependencies ที่ต้องมี

ตอนนี้โปรเจกต์ใช้ package เพิ่มเติมนอกเหนือจาก Flask เช่น:
- `Flask-Bcrypt`
- `Flask-Cors`
- `google-auth`
- `gunicorn`
- `PyMySQL`

ทั้งหมดถูกเพิ่มไว้ใน [requirements.txt](/Users/kitty/Desktop/C/backend/requirements.txt) แล้ว

## เช็กหลัง deploy

หลัง deploy สำเร็จ ให้เปิด URL ของ Railway แล้วทดสอบ path หลัก:

```bash
GET /
```

ควรได้ response ประมาณนี้:

```json
{"message":"Flask + MySQL Ready!222"}
```
