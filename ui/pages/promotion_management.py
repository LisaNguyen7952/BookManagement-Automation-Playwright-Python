from ui.pages.base_page import BasePage


class PromotionManagement(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.promotion_management_option = self.page.locator("span",has_text="Promotion")
        self.promotion_page_title = self.page.locator("h4",has_text="Promotion Management")


