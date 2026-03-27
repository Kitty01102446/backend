"""
แอพหลัก (entrypoint) ของโปรเจค

ไฟล์นี้อ่านค่าจาก .env, สร้าง Flask app และลงทะเบียน Blueprints
คอมเมนต์ทั้งหมดเป็นภาษาไทยตามคำขอของผู้ใช้
"""

from dotenv import load_dotenv
from flask import Flask, request
from flask_cors import CORS
from flask_bcrypt import Bcrypt


# โหลดตัวแปร environment จากไฟล์ .env (ถ้ามี)
load_dotenv()

bcrypt = Bcrypt()

def create_app():
    """สร้าง Flask application และลงทะเบียน blueprints (controllers)

    คืนค่า Flask app ที่พร้อมใช้งาน
    """
    app = Flask(__name__)
    
    bcrypt.init_app(app)


    # ******************************************************
    # 💡 การตั้งค่า CORS (สำคัญมากในการแก้ปัญหาที่เกิดขึ้นก่อนหน้านี้)
    # อนุญาตให้ Client (React) ที่รันบน http://localhost:5174 สามารถเรียก API ได้
    # หาก React รันบน Port อื่น เช่น 3000 หรือ 8080 ให้เปลี่ยนเลข Port ที่นี่
    CORS(app, resources={r"/*": {"origins": "*"}}) 
    # ใช้ r"/*" หมายถึงทุกเส้นทาง (routes) ในแอพนี้จะถูกใช้ CORS
    # ******************************************************

    # ลงทะเบียน blueprints ที่อยู่ในโฟลเดอร์ controllers
    try:
        from controllers.product_controller import products_bp
        from controllers.users_controller import users_bp
        from controllers.address_controller import address_bp
        from controllers.bill_controller import bill_bp
        from controllers.employee_controller import employee_bp
        from controllers.favorite_controller import favorite_bp
        from controllers.payment_controller import payment_bp
        from controllers.permission_controller import permission_bp
        from controllers.promotion_controller import promotion_bp
        from controllers.review_controller import review_bp
        from controllers.role_controller import role_bp
        from controllers.role_permission_controller import role_permission_bp
        from controllers.service_controller import service_bp
        from controllers.status_booking_controller import status_booking_bp
        from controllers.status_service_controller import status_service_bp
        from controllers.status_store_controller import status_store_bp
        from controllers.store_controller import store_bp
        from controllers.store_address_controller import store_address_bp
        from controllers.token_controller import token_bp
        from controllers.type_booking_controller import type_booking_bp
        from controllers.type_promo_controller import type_promo_bp
        from controllers.type_service_controller import type_service_bp
        from controllers.click_log_controller import click_log_bp
        from controllers.booking_controller import booking_bp


        print("📌 employee_controller loaded")

        app.register_blueprint(products_bp)
        app.register_blueprint(users_bp)
        app.register_blueprint(address_bp)
        app.register_blueprint(bill_bp)
        app.register_blueprint(employee_bp)
        app.register_blueprint(favorite_bp)
        app.register_blueprint(payment_bp)
        app.register_blueprint(permission_bp)
        app.register_blueprint(promotion_bp)
        app.register_blueprint(review_bp)
        app.register_blueprint(role_bp)
        app.register_blueprint(role_permission_bp)
        app.register_blueprint(service_bp)
        app.register_blueprint(status_booking_bp)
        app.register_blueprint(status_service_bp)
        app.register_blueprint(status_store_bp)
        app.register_blueprint(store_bp)
        app.register_blueprint(store_address_bp)
        app.register_blueprint(token_bp)
        app.register_blueprint(type_booking_bp)
        app.register_blueprint(type_promo_bp)
        app.register_blueprint(type_service_bp)
        app.register_blueprint(click_log_bp)
        app.register_blueprint(booking_bp)



    except Exception as e:
        print("❌ booking_controller failed::", e)
        raise

    @app.before_request
    def log_request_start():
        # บันทึก request ที่เข้ามาเพื่อดูจาก Railway logs ได้ทันที
        print(f"➡️ {request.method} {request.path}")

    @app.route("/")
    def home():
        # หน้าเริ่มต้น เพื่อยืนยันว่าแอพพร้อมใช้งาน
        return {"message": "Flask + MySQL Ready!222"}

    @app.route("/health")
    def health():
        # route เบา ๆ สำหรับเช็กว่า worker ตอบ request ได้จริง
        return {"status": "ok"}, 200

    return app


# 💡 ส่วนนี้จะถูกใช้รันใน Development Mode
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, port=5010) # กำหนด port ชัดเจน (สมมติว่าเป็น 5000)

# 💡 ส่วนนี้จะถูกใช้รันใน Production/Staging (ด้วย Gunicorn/uWSGI)
# Gunicorn จะอ้างอิงถึงตัวแปร 'app' นี้เพื่อนำไปรัน
app = create_app()
