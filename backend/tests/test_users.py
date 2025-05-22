from fastapi.testclient import TestClient

from backend.main import app
from backend.schemas import User

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
