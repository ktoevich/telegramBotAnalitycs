FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Bot database will be written to /data (mounted as PVC)
WORKDIR /data
CMD ["python", "/app/main.py"]
