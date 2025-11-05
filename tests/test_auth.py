import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True)
def create_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_register_and_login():
    resp = client.post("/register", json={"username":"test", "email":"t@example.com", "password":"abc1234"})
    assert resp.status_code == 201
    resp2 = client.post("/login", json={"username":"test", "password":"abc1234"})
    assert resp2.status_code == 200
    assert "access_token" in resp2.json()
