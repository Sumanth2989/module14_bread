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

    # --- Wait for navigation after clicking submit ---
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE_URL}/login", timeout=10000)  # wait up to 10s

    # Confirm URL is /login
    expect(page).to_have_url(f"{BASE_URL}/login")

def test_login_positive(page: Page):
    email = make_unique_email()
    password = "password123"[:72]  # truncate to 72 bytes

    # 1. Register first
    page.goto(f"{BASE_URL}/register")
    page.fill('input[name="email"]', email)
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE_URL}/login", timeout=10000)

    # 2. Now login
    page.goto(f"{BASE_URL}/login")
    page.fill('input[name="username"]', email)  # or 'email' if your form uses that
    page.fill('input[name="password"]', password)
    page.click('button[type="submit"]')
    page.wait_for_url(f"{BASE_URL}/calculations", timeout=10000)

    # Confirm URL is /calculations
    expect(page).to_have_url(f"{BASE_URL}/calculations")
