import pytest
from playwright.sync_api import Page, expect
from app.auth import get_password_hash
from app.models.user import User
from app.db import get_db

BASE_URL = "http://localhost:8000"

def ensure_test_user(db):
    # Create user if not exists
    test_email = "testuser@example.com"
    test_password = "password123"[:72]  # truncate for bcrypt
    existing_user = db.query(User).filter(User.email == test_email).first()
    if not existing_user:
        user = User(email=test_email, hashed_password=get_password_hash(test_password))
        db.add(user)
        db.commit()
        db.refresh(user)
    return test_email, test_password

def test_bread_operations(page: Page, db=get_db()):
    TEST_USERNAME, TEST_PASSWORD = ensure_test_user(db)
    
    # 1. LOGIN
    page.goto(f"{BASE_URL}/login")
    page.fill("input[name='username']", TEST_USERNAME)
    page.fill("input[name='password']", TEST_PASSWORD)
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle") 

    expect(page).to_have_url(f"{BASE_URL}/calculations")
    expect(page.locator("body")).to_contain_text("My Calculations")
    
    # 2. ADD (Create)
    page.goto(f"{BASE_URL}/calculations/add")
    page.fill("input[name='operand1']", "10")
    page.select_option("select[name='operation']", "add")
    page.fill("input[name='operand2']", "5")
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
    
    # 3. Check result (Read/Browse)
    expect(page.locator("body")).to_contain_text("15.0")
    
    # 4. EDIT (Update)
    page.click("text=Edit")
    page.fill("input[name='operand1']", "20")
    page.select_option("select[name='operation']", "add")
    page.click("button[type='submit']")
    page.wait_for_load_state("networkidle")
    expect(page.locator("body")).to_contain_text("25.0")
    
    # 5. DELETE
    page.once("dialog", lambda dialog: dialog.accept())
    page.click("text=Delete")
    page.wait_for_load_state("networkidle")
    expect(page.locator("body")).not_to_contain_text("25.0")
