FROM python:3.9-slim-buster

WORKDIR /app2

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/backend backend

CMD ["sh", "-c", "pytest backend/backend/tests && uvicorn backend.main:app --host 0.0.0.0 --port 8000"]

# CMD ["ls", "-lah"]
