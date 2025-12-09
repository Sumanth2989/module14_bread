from sqlalchemy.orm import Session
from app.models.calculation import Calculation, CalculationType
from app.models.user import User
from app.services.calculation_service import create_calculation
from app.schemas.calculation import CalculationCreate
from app.auth import get_password_hash

def test_create_calculation_persists_in_db(db_session: Session):
    """
    Ensure that creating a calculation via the service persists it in the database.
    """
    # 1️⃣ Create a test user dynamically
    test_user = User(
        email="testuser@example.com",
        hashed_password=get_password_hash("password123"[:72])  # truncate for bcrypt
    )
    db_session.add(test_user)
    db_session.commit()
    db_session.refresh(test_user)

    # 2️⃣ Create the input calculation
    calc_in = CalculationCreate(a=10, b=5, type=CalculationType.DIVISION)
    
    # 3️⃣ Call the service function using the actual user_id
    created = create_calculation(db_session, calc_in, user_id=test_user.id)
    
    # 4️⃣ Assertions
    assert created.id is not None
    assert created.result == 2

    # 5️⃣ Check directly from DB
    from_db = db_session.query(Calculation).filter(Calculation.id == created.id).first()
    assert from_db is not None
    assert from_db.a == 10
    assert from_db.b == 5
    assert from_db.type == CalculationType.DIVISION
    assert from_db.result == 2
