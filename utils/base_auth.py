import os

from pytest_playwright.pytest_playwright import playwright

from configs.env_config import BASE_URL, EMAIL, PASSWORD
from configs.other_config import STORAGE_STATE, STORAGE_DIR
from ui.pages.log_in_page import LoginPage

def login_and_save_storage(playwright):
    os.makedirs(STORAGE_DIR, exist_ok=True)

    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()

    log_in(page)

    print(page.evaluate("() => Object.keys(localStorage)"))
    print(page.evaluate("() => localStorage"))

    context.storage_state(path=STORAGE_STATE)

    context.close()
    browser.close()
def ensure_storage_state(playwright):
    if not os.path.exists(STORAGE_STATE):
        login_and_save_storage(playwright)
        return

    browser = playwright.chromium.launch()
    context = browser.new_context(storage_state=STORAGE_STATE)
    page = context.new_page()

    page.goto(BASE_URL)

    valid = is_session_valid(page)

    context.close()
    browser.close()

    if not valid:
        os.remove(STORAGE_STATE)
        login_and_save_storage(playwright)

def log_in(page):
    page.goto(BASE_URL)

    login_page = LoginPage(page)

    # email_input = page.locator("input[name='email']")

    try:
        login_page.navigate_to_login_page()
        assert login_page.view_login_page(), f"unable to navigate to login page"

        login_page.login(EMAIL, PASSWORD)
        if login_page.view_base_url():
            print(f"Navigate to base url after login properly")
        assert "login successfully" in login_page.get_alert_text().lower(), f"incorrectly alert, please recheck  refer to this alert - {login_page.get_alert_text()}"
        print(f"Login successfully")

    except:
        print("⚠️ Login form not found → probably already logged in")

def is_session_valid(page):
    try:

        page.goto(BASE_URL)

        page.wait_for_load_state("networkidle")

        cookies = page.context.cookies()

        return len(cookies) > 0

    except:
        return False