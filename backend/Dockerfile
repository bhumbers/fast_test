FROM python:3.9-slim-buster AS builder

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend backend

FROM builder AS test

ENV PYTHONPATH "${PYTHONPATH}:/app/backend"
COPY tests tests

CMD ["pytest", "tests"]

FROM builder AS service

ENV PYTHONPATH "${PYTHONPATH}:/app/backend"

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
