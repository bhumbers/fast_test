from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.main import app, get_db
from backend.models import Base
from backend.schemas import UserCreate, User
from backend.database import SessionLocal

Base.metadata.create_all(bind=SessionLocal)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_and_read_user():
    user_data = {
        "email": "test@example.com",
        "password": "password123",
        "username": "testuser"
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200, response.text
    created_user = User(**response.json())
    assert created_user.email == user_data["email"]
    assert created_user.username == user_data["username"]

    response = client.get(f"/users/{created_user.id}")
    assert response.status_code == 200, response.text
    read_user = User(**response.json())
    assert read_user.id == created_user.id
    assert read_user.email == created_user.email
    assert read_user.username == created_user.username
