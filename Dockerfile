FROM python:3.12-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# 暴露 Django 預設埠口
EXPOSE 8000

# 使用 gunicorn 啟動（生產環境建議），或先用 runserver 測試
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]s