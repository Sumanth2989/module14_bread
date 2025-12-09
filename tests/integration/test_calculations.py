from fastapi.testclient import TestClient
from app.main import app
from app.deps import get_current_user # Need this to override
from app.models.user import User # Need this for the dummy user

client = TestClient(app)

# 1. Create a dummy user object
DUMMY_USER = User(id=1, email="test@test.com", hashed_password="hashed")

# 2. Create the override function
def override_get_current_user():
    return DUMMY_USER

# 3. Apply the override to the client
app.dependency_overrides[get_current_user] = override_get_current_user

def test_calculation_bread_flow():
    create_payload = {"operand1": 10, "operand2": 5, "operation": "add"}

    # NOTE: The test now runs AS DUMMY_USER
    r = client.post("/calculations/add", data=create_payload, follow_redirects=False)
    assert r.status_code == 303