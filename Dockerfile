FROM python:3.10-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

RUN chmod +x /app/mtu.py

ENTRYPOINT ["python", "/app/mtu.py"]
