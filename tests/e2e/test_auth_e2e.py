import pytest
from playwright.sync_api import Page, expect
import random

BASE_URL = "http://localhost:8000"

def make_unique_email():
    return f"test_{random.randint(1000, 9999)}@example.com"

def test_register_positive(page: Page):
    email = make_unique_email()
    
    page.goto(f"{BASE_URL}/register")
    
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', "password123")
    
    # --- FIX 1: Wait for navigation after registration submission ---
    with page.expect_navigation():
        page.click('button[type="submit"]')
    
    # After registering, it should redirect to login
    expect(page).to_have_url(f"{BASE_URL}/login")

def test_login_positive(page: Page):
    email = make_unique_email()
    password = "password123"
    
    # 1. Register first
    page.goto(f"{BASE_URL}/register")
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    
    # Wait for navigation after registration
    with page.expect_navigation():
        page.click('button[type="submit"]')
    
    # 2. Now Login (should be at /login already, but we navigate explicitly)
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="username"]', email)
    page.fill('input[name="password"]', password)
    
    # --- FIX 2: Wait for navigation after login submission ---
    with page.expect_navigation():
        page.click('button[type="submit"]')
    
    # Expect redirect to calculations list
    expect(page).to_have_url(f"{BASE_URL}/calculations")