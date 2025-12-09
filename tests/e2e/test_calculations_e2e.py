import pytest
from playwright.sync_api import Page, expect
import time # Time is still used for the sleep trick if necessary, but we try to avoid it

BASE_URL = "http://localhost:8000"

def test_bread_operations(page: Page):
    TEST_USERNAME = "testuser@example.com"
    TEST_PASSWORD = "password123"
    
    # 1. LOGIN
    page.goto(f"{BASE_URL}/login")
    page.fill("input[name='username']", TEST_USERNAME)
    page.fill("input[name='password']", TEST_PASSWORD)
    
    # --- FIX 1: Wait for navigation after login submission ---
    # Using page.press("Enter") is the most robust way to trigger the submission event.
    with page.expect_navigation():
        page.press("input[name='password']", "Enter") 
    
    # Verify we successfully redirected to the calculations page
    expect(page).to_have_url(f"{BASE_URL}/calculations")
    expect(page.locator("body")).to_contain_text("My Calculations")
    
    # 2. ADD (Create)
    page.goto(f"{BASE_URL}/calculations/add") 
    page.fill("input[name='operand1']", "10")
    page.select_option("select[name='operation']", "add")
    page.fill("input[name='operand2']", "5")
    
    # Wait for navigation after creation submission
    with page.expect_navigation():
        page.click("button[type='submit']")
    
    # 3. Check result (Read/Browse)
    expect(page.locator("body")).to_contain_text("15.0")

    # 4. EDIT (Update) 
    page.click("text=Edit")
    page.fill("input[name='operand1']", "20") 
    
    # Fix from previous step: Explicitly select 'add' during the edit 
    page.select_option("select[name='operation']", "add") 
    
    # Wait for navigation after edit submission
    with page.expect_navigation():
        page.click("button[type='submit']")
        
    expect(page.locator("body")).to_contain_text("25.0")
    
    # 5. DELETE
    page.once("dialog", lambda dialog: dialog.accept()) 
    page.click("text=Delete")
    expect(page.locator("body")).not_to_contain_text("25.0")