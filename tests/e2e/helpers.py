import random
from app.models.user import User
from app.auth import get_password_hash

def ensure_test_user(db):
    """
    Creates a test user with a unique email every time.
    Returns (email, password).
    """
    # Generate a unique email
    email = f"test_{random.randint(1000, 9999)}@example.com"
    password = "password123"[:72]  # truncate for bcrypt/argon2

    # Check if this exact email somehow exists
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        user = User(email=email, hashed_password=get_password_hash(password))
        db.add(user)
        try:
            db.commit()
        except Exception:
            db.rollback()
            # fallback: pick another random email if collision occurs
            return ensure_test_user(db)
        db.refresh(user)

    return email, password
