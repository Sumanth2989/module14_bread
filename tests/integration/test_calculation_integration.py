from sqlalchemy.orm import Session
from app.models.calculation import Calculation, CalculationType
from app.services.calculation_service import create_calculation
from app.schemas.calculation import CalculationCreate


def test_create_calculation_persists_in_db(db_session: Session):
    """
    Ensure that creating a calculation via the service persists it in the database.
    """

    # Create the input object using the schema's names
    calc_in = CalculationCreate(a=10, b=5, type=CalculationType.DIVISION)
    
    # Call the service function and assign the returned object
    created = create_calculation(db_session, calc_in, user_id=1) 
    
    # Check returned object
    assert created.id is not None
    assert created.result == 2

    # Check directly from DB
    from_db = db_session.query(Calculation).filter(Calculation.id == created.id).first()
    assert from_db is not None
    assert from_db.a == 10
    assert from_db.b == 5
    assert from_db.type == CalculationType.DIVISION
    assert from_db.result == 2


def test_create_calculation_persists_in_db(db_session: Session):
    # Create the input object using the schema's names (a, b)
    calc_in = CalculationCreate(a=10, b=5, type=CalculationType.DIVISION)
    
    # --- THE MISSING LINE: Assign the function output to 'created' ---
    created = create_calculation(db_session, calc_in, user_id=1) 
    
    # Check returned object
    assert created.id is not None
