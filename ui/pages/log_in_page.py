from assertions.ui_assertions import is_locator_visible
from ui.pages.base_page import BasePage
from utils.interactions import safe_fill, safe_click

class LoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.login_icon = self.page.locator("//div[@class='MuiBox-root css-swawqt']/button")
        self.email_field = self.page.locator("input[name='email']")
        self.password_field = self.page.locator("input[name='password']")
        self.login_account_button = self.page.get_by_text("Login account")

    def view_base_url(self):
        return is_locator_visible(self.login_icon)

    def navigate_to_login_page(self):
        safe_click(self.login_icon)
    def view_login_page(self):
        return is_locator_visible(self.login_account_button)
    def login(self,email,password):
        safe_fill(self.email_field,email)
        safe_fill(self.password_field,password)
        self.login_account_button.click()



