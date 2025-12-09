from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.auth import hash_password, verify_password

router = APIRouter(
    prefix="/users",
    tags=["users"],
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if email already exists
    existing = db.query(User).filter(User.email == user_in.email).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered",
        )

    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password[:72]),  # truncate to 72 bytes
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # Redirect to /login after successful registration
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/login", response_model=UserRead)
def login(user_in: UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == user_in.email).first()
    if not user or not verify_password(user_in.password[:72], user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email or password",
        )

    # Return user for now; tokens can be added later
    return user
