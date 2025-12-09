from fastapi import APIRouter, Depends, HTTPException, status, Response, Request, Form
from sqlalchemy.orm import Session
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from app.db import get_db
from app.models.user import User
from app.auth import authenticate_user, create_access_token, get_password_hash
from app.schemas.user import UserRead

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# ----------------------------
# LOGIN ROUTES
# ----------------------------
@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
def login(
    response: Response,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": response, "error": "Invalid credentials"})

    access_token = create_access_token(data={"sub": str(user.id)})
    response = RedirectResponse(url="/calculations", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

# ----------------------------
# LOGOUT ROUTE
# ----------------------------
@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=303)
    response.delete_cookie("access_token")
    return response

# ----------------------------
# BROWSER REGISTRATION ROUTES (for frontend / E2E)
# ----------------------------
@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register")
def register(
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
    request: Request = None
):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        return templates.TemplateResponse("register.html", {"request": request, "error": "Email already registered"})

    hashed_pwd = get_password_hash(password[:72])  # truncate to 72 bytes
    new_user = User(email=email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Redirect to login page for browser workflow
    return RedirectResponse(url="/login", status_code=303)

# ----------------------------
# API REGISTRATION ROUTE (for pytest integration)
# ----------------------------
@router.post("/api/register", status_code=status.HTTP_201_CREATED, response_model=UserRead)
def api_register(email: str, password: str, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pwd = get_password_hash(password[:72])  # truncate to 72 bytes
    new_user = User(email=email, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user  # JSON response for integration tests
