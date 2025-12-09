import pytest
from playwright.sync_api import Page, expect
import random

BASE_URL = "http://localhost:8000"

def make_unique_email():
    return f"test_{random.randint(1000, 9999)}@example.com"

def test_register_positive(page: Page):
    email = make_unique_email()
    password = "password123"[:72]  # truncate to 72 bytes

    page.goto(f"{BASE_URL}/register")
    
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    
    # Wait for redirect to login
    with page.expect_navigation():
        page.click('button[type="submit"]')
    
    expect(page).to_have_url(f"{BASE_URL}/login")

def test_login_positive(page: Page):
    email = make_unique_email()
    password = "password123"[:72]  # truncate to 72 bytes

    # 1. Register first
    page.goto(f"{BASE_URL}/register")
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    
    with page.expect_navigation():
        page.click('button[type="submit"]')
    
    # 2. Login
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="email"]', email)  # <-- changed from username to email
    page.fill('input[name="password"]', password)
    
    with page.expect_navigation():
        page.click('button[type="submit"]')
    
    expect(page).to_have_url(f"{BASE_URL}/calculations")
