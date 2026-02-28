import os
import uuid

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from app.database import Base, get_db
from app.main import app


SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
Base.metadata.create_all(bind=engine)
client = TestClient(app)


def test_create_and_get_user():
    unique_email = f"test-{uuid.uuid4().hex[:8]}@example.com"
    payload = {
        "email": unique_email,
        "full_name": "Test User",
        "password": "StrongPass123",
    }

    create_response = client.post("/api/v1/users/", json=payload)
    assert create_response.status_code == 201

    user_id = create_response.json()["id"]
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == 200
    assert get_response.json()["email"] == payload["email"]
