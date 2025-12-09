from fastapi.testclient import TestClient
from app.main import app
import random # Add this import!

client = TestClient(app)

def make_unique_email():
    # Helper function to generate a unique email
    return f"test_user_{random.randint(1000, 9999)}@example.com"

def test_register_and_login_user():
    # Use unique email so repeated runs don't fail
    unique_email = make_unique_email()
    payload_register = {"email": unique_email, "password": "shortpassword"} # Use unique email here!

    # Register (This must now return 201)
    r = client.post("/users/register", json=payload_register)
    # The test must fail if registration fails, so assert only 201
    assert r.status_code == 201 

    # Prepare login payload
    payload_login = {
        "email": payload_register["email"],
        "password": payload_register["password"]
    }
    
    # Login (Send as JSON payload)
    r2 = client.post(
        "/users/login",
        json=payload_login
    )
    
    # Check success (200 OK)
    assert r2.status_code == 200
    
    # Check returned data
    data = r2.json()
    assert data["email"] == payload_register["email"]
    assert "id" in data