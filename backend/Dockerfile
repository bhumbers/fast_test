FROM python:3.9-slim-buster AS builder

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/backend backend

FROM builder AS test

CMD ["pytest", "backend/backend/tests"]

FROM builder AS service

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
