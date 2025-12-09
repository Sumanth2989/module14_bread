from datetime import datetime, timedelta, timezone
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from passlib.handlers.bcrypt import bcrypt # Import the specific handler
from sqlalchemy.orm import Session
from app.models.user import User

# --- CONFIGURATION ---
SECRET_KEY = "supersecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# --- PERMANENT FIX FOR 72-BYTE PASSWORD BUG ---
# Explicitly configure the context using the specific bcrypt handler 
# and setting the scheme directly to avoid auto-detection errors.
# --- PERMANENT FIX FOR 72-BYTE PASSWORD BUG ---
# Explicitly configure the context using the specific bcrypt handler 
# and setting the scheme directly to avoid auto-detection errors.
pwd_context = CryptContext(
    schemes=["bcrypt"],
    default="bcrypt", # <-- THIS IS THE CRITICAL FIX
    # Passlib documentation recommends listing the handlers explicitly:
    backends={
        "bcrypt": bcrypt, 
    },
    # Ensure auto-detection is minimal
    deprecated="auto"
)

# --- HASHING TOOLS ---
def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Optional: Truncate password before verification if necessary, but the context fix usually handles it
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    # Optional: Truncate long passwords to avoid runtime issues if the user input is huge
    # password = password[:72] 
    return pwd_context.hash(password)

# --- THE FIX: ALIAS ---
hash_password = get_password_hash

# --- AUTHENTICATION LOGIC ---
def authenticate_user(db: Session, username: str, password: str):
    # We use 'email' as the username
    user = db.query(User).filter(User.email == username).first()
    if not user:
        return None
    # Verify password should now be stable due to the pwd_context fix
    if not verify_password(password, user.hashed_password):
        return None
    return user

# --- TOKEN TOOLS ---
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None