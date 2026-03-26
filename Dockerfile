FROM python:3.11-slim

# ตั้ง working dir
WORKDIR /app

# copy requirements ก่อน (เร็วขึ้น)
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy code ทั้งหมด
COPY . .

# expose port (Railway ใช้ PORT env)
EXPOSE 5000

# run app ด้วย gunicorn (สำคัญมาก)
CMD ["sh", "-c", "gunicorn -b 0.0.0.0:$PORT app:app"]