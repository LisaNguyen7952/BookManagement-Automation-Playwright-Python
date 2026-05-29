from configs.env_config import PASSWORD, EMAIL
from configs.other_config import INVALID_EMAIL, INVALID_PASSWORD
from ui.pages.log_in_page import LoginPage
from utils.logger_helper import get_logger

logger = get_logger()
def test_log_in_success(page):
    log_in= LoginPage(page)
    log_in.navigate_to_login_page()
    assert log_in.view_login_page(),f"unable to navigate to login page"
    log_in.login(EMAIL,PASSWORD)
    if log_in.view_base_url():
        print(f"Navigate to base url after login properly")
    assert "login successfully" in log_in.get_alert_text().lower(), f"incorrectly alert, please recheck  refer to this alert - {log_in.get_alert_text()}"
    logger.info(f"Login successfully")

def test_log_in_by_invalid_email(page):
    log_in= LoginPage(page)
    log_in.navigate_to_login_page()
    assert log_in.view_login_page(), f"unable to navigate to login page"
    log_in.login(INVALID_EMAIL, PASSWORD)
    if not log_in.view_base_url():
        print(f"Do not navigate to base url after login fail correctly")
    logger.info(f"Unable log in with invalid email properly and refer to this alert - {log_in.get_alert_text()}")


def test_log_in_by_invalid_password(page):
    log_in= LoginPage(page)
    log_in.navigate_to_login_page()
    assert log_in.view_login_page(), f"unable to navigate to login page"
    log_in.login(EMAIL, INVALID_PASSWORD)
    if not log_in.view_base_url():
        print(f"Do not navigate to base url after login fail correctly")
    logger.info(f"Unable log in with invalid email properly and refer to this alert - {log_in.get_alert_text()}")