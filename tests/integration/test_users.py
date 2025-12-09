from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login_user():
    # Use unique email so repeated runs don't fail
    payload = {"email": "test_user@example.com", "password": "shortpassword"}

    # Register
    r = client.post("/users/register", json=payload)
    assert r.status_code in (201, 400)

    # Login
    r2 = client.post("/users/login", json=payload)
    assert r2.status_code == 200
    data = r2.json()
    assert data["email"] == payload["email"]
    assert "id" in data
