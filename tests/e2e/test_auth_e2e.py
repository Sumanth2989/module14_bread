import pytest
from playwright.sync_api import Page, expect
from app.db import get_db
from app.models.user import User
from app.auth import get_password_hash
import random

BASE_URL = "http://localhost:8000"

def make_unique_email():
    return f"test_{random.randint(1000, 9999)}@example.com"

def ensure_user(db, email, password):
    """Create the user if it doesn't exist (truncate password for bcrypt)"""
    password = password[:72]  # truncate to 72 bytes
    existing_user = db.query(User).filter(User.email == email).first()
    if not existing_user:
        user = User(email=email, hashed_password=get_password_hash(password))
        db.add(user)
        db.commit()
        db.refresh(user)
    return email, password

def test_register_positive(page: Page, db=get_db()):
    email = make_unique_email()
    password = "password123"[:72]

    # Go to register page
    page.goto(f"{BASE_URL}/register")
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_load_state("networkidle")

    # After registration, should redirect to login
    expect(page).to_have_url(f"{BASE_URL}/login")

    # Ensure user is actually in DB
    user_in_db = db.query(User).filter(User.email == email).first()
    assert user_in_db is not None

def test_login_positive(page: Page, db=get_db()):
    email = make_unique_email()
    password = "password123"[:72]
    
    # Make sure user exists
    ensure_user(db, email, password)
    
    # Go to login page
    page.goto(f"{BASE_URL}/login")
    page.fill("input[name='username']", email)
    page.fill("input[name='password']", password)
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
    
    # Should redirect to calculations page
    expect(page).to_have_url(f"{BASE_URL}/calculations")
