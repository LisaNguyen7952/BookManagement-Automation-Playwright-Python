import os
from datetime import datetime

import allure
import pytest

from playwright.sync_api import sync_playwright

from api.services.auth_service import AuthService
from assertions.api_assertions import assert_status
from configs.env_config import BASE_URL, TIMEOUT, EMAIL, PASSWORD
from configs.other_config import STORAGE_STATE, SCREENSHOT_DIR, VIEWTRACE_DIR
from core.api_client import APIClient
from utils.base_auth import ensure_storage_state


# ==========================
# API CLIENT (GIỮ NGUYÊN - SYNC OK)
# ==========================

@pytest.fixture(scope="session")
def api_client(playwright):

    request_context = playwright.request.new_context(
        base_url=BASE_URL,
        timeout=TIMEOUT,
        ignore_https_errors=True
    )

    client = APIClient(
        request=request_context,
        base_url=BASE_URL,
        timeout=TIMEOUT
    )

    yield client
    request_context.dispose()


@pytest.fixture(scope="session")
def auth_token(api_client):
    auth_service = AuthService(api_client)

    response = auth_service.login(EMAIL, PASSWORD)
    assert_status(response, 200)

    return response.json().get("accessToken")


@pytest.fixture
def authorized_client(api_client, auth_token):
    api_client.set_token(auth_token)
    yield api_client
    api_client.token = None


# ==========================
# PLAYWRIGHT SYNC FIXTURES
# ==========================

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as p:
        yield p

@pytest.fixture(scope="session")
def browser(playwright_instance):

    ensure_storage_state(playwright_instance)

    browser = playwright_instance.chromium.launch(headless=False)

    yield browser

    browser.close()

@pytest.fixture(scope="function")
def context(browser):

    context = browser.new_context(
        storage_state=STORAGE_STATE
    )

    context.tracing.start(
        screenshots=True,
        snapshots=True,
        sources=True,
    )

    yield context

    # KHÔNG close ở đây


@pytest.fixture
def page(context):

    page = context.new_page()

    page.goto(BASE_URL)

    yield page


# ==========================
# HELPERS (SYNC)
# ==========================

def take_screenshot(page, test_name):
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    file_path = os.path.join(SCREENSHOT_DIR, f"{test_name}_{timestamp}.png")
    page.screenshot(path=file_path, full_page=True)

    return file_path


def save_view_trace(context, test_name):
    os.makedirs(VIEWTRACE_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    file_path = os.path.join(VIEWTRACE_DIR, f"{test_name}_{timestamp}.zip")
    try:
        context.tracing.stop(path=file_path)
    except Exception:
        print(f"Failed to save trace, tracing might not start yet")

    return file_path


# ==========================
# HOOK (SYNC VERSION)
#
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    page = item.funcargs.get("page")
    context = item.funcargs.get("context")
    test_name = item.name

    try:

        if report.failed:

            if page:
                screenshot_path = take_screenshot(page, test_name)

                allure.attach.file(
                    screenshot_path,
                    name="screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

            if context:
                trace_path = save_view_trace(context, test_name)

                allure.attach.file(
                    trace_path,
                    name="trace",
                    attachment_type="application/zip"
                )

        else:
            if context:
                context.tracing.stop()

    finally:

        # ✅ close tại đây
        if page:
            page.close()

        if context:
            context.close()