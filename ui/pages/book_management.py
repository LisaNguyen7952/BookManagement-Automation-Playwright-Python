import re

from assertions.ui_assertions import is_locator_visible, is_locator_invisible, is_locator_checked
from ui.pages.base_page import BasePage
from utils.interactions import get_locator_text, is_tab_selected, get_locator_texts, \
    get_locator_attribute_texts, get_locator_attribute_text, \
    select_multiple_dropdown_values
from utils.logger_helper import logger


class UIBookManagement(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.book_management_option = self.page.locator("//div[@class='simplebar-content']/nav/ul/li/a[.='Book']")
        self.book_management_title = self.page.locator("h4", has_text="Book Management")
        self.add_book_button = self.page.locator("a",has_text="New Book")
        self.book_title_page = self.page.locator("li", has_text="Create a new book")
        self.book_name_field = self.page.locator("//input[@name='name']")
        self.slug_name_field = self.page.locator("//input[@name='slug']")
        self.change_checkbox = self.page.locator("button",has_text="Change")
        self.description_field = self.page.locator("//div/textarea[@name='description']")
        self.price_field = self.page.locator("//input[@name='price']")
        self.categories_dropdown = self.page.locator("//input[@role='combobox']")
        self.promotion_selection_icon  = self.page.locator("//span[text()='Promotion']/ancestor::div[contains(@class,'MuiCardHeader-root')]//button")
        self.promotion_search_textbox = self.page.get_by_placeholder("Search...")
        self.promotion_checkbox = self.page.locator("//td//input[@type='checkbox']")

        self.create_book_button = self.page.locator("button",has_text="Create book")
        self.save_changes_button = self.page.locator("button",has_text="Save changes")
        self.delete_button = self.page.locator("button",has_text="Delete")
        self.delete_title_popup = self.page.locator("h2", has_text="Confirm delete")
        self.confirm_delete_button = self.page.locator("#dialog-delete-action")

        self.add_files = self.page.locator("//input[@name='picture']")

        self.uploaded_files = self.page.locator("//input[@name='picture']/ancestor::div[1]/div[2]/div")
        self.categories_field= self.page.locator("//div[@role='button']/span/div")

        self.category_tabs = self.page.locator("//button[@role='tab']")
        self.book_names = self.page.locator("//a/h6")
    def get_category_tab_list(self):
        category_list_raw =  get_locator_texts(self.category_tabs)
        return [re.sub(r"\s+\d+$","",text).rstrip()
                for text in category_list_raw]

    def specific_category_tab_by_its_name(self, category: str):
        return self.page.locator(
            f"//button[@role='tab'][.//*[normalize-space(text())='{category}']]"
        )

    def book_number_by_category(self, category: str):
        return self.specific_category_tab_by_its_name(category).locator("span")
    def specific_book(self, book_name):
        return self.page.locator("//a/h6", has_text=f"{book_name}")
    def specific_book_adjustment_icon(self,book_name):
        return self.specific_book(book_name).locator("xpath=ancestor::div[1]").locator("button")
    def price_for_specific_book(self,book_name):
        return self.page.specific_book(book_name).locator(".//div/h6")

    def view_book_management(self):
        self.book_management_option.click()
    def is_book_management_page_visible(self):
        return is_locator_visible(self.book_management_title)
    def view_book_category_tab(self, category: str):
        self.specific_category_tab_by_its_name(category).click()
    def is_book_category_tab_selected(self, category: str):
        return is_tab_selected(self.specific_category_tab_by_its_name(category))
    def get_number_of_books_for_specific_category(self,category: str):
        return int(get_locator_text(self.book_number_by_category(category)))
    def get_number_of_books_currently_showing(self):
        return self.book_names.count()
    def get_book_list_currently_showing(self):
        return get_locator_texts(self.book_names)

    def view_specific_book_detail(self,book_name):
        self.specific_book_adjustment_icon(book_name).click()

    def get_book_detail(self):
        book_name = get_locator_attribute_text(self.book_name_field, "value")
        book_slug_name = get_locator_attribute_text(self.slug_name_field, "value")
        book_description = get_locator_text(self.description_field)
        book_price = int(get_locator_attribute_text(self.price_field,"value"))
        book_promotions = self.get_promotions()
        book_pictures = self.get_uploaded_files()
        book_categories = self.get_categories()
        book_detail = {
            "name": book_name,
            "price": book_price,
            "description": book_description,
            "pictures": book_pictures,
            "promotions": book_promotions,
            "slug": book_slug_name,
            "categories": book_categories,
        }
        return book_detail
    def get_categories(self):
        raw_categories = get_locator_texts(self.categories_field)
        return [
            re.sub(r"^\d+","",v).strip()
            for v in raw_categories
        ]
    def get_uploaded_files(self):
        raw = get_locator_attribute_texts(self.uploaded_files, "aria-label")
        return [re.sub(r"_[a-zA-Z0-9]{4}(?=\.)","",v)
        for v in raw]
    def view_add_new_book_page(self):
        self.add_book_button.click()
    def is_book_detail_page_visible(self):
        return is_locator_visible(self.book_title_page)
    def is_add_new_book_page_invisible(self):
        return is_locator_invisible(self.book_title_page)
    def input_new_book_info(self, book_info:dict):
        if book_info["name"]:
            self.book_name_field.fill(book_info["name"])
        if book_info.get("slug"): #slug ís optional
            self.change_checkbox.click()
            self.slug_name_field.fill(book_info["slug"])
        if book_info["description"]:
            self.description_field.fill(book_info["description"])
        if book_info["pictures"]:
            upload_multiple_files_one_by_one(self.add_files,book_info["pictures"])
        if book_info["price"]:
            self.price_field.fill(str(book_info["price"]))
        if book_info["categories"]:
            select_multiple_dropdown_values(self.categories_dropdown, book_info["categories"])
        if book_info["promotions"]:
            self.promotion_selection_icon.click()
            if not is_locator_visible(self.promotion_search_textbox):
                logger.warning(f"Unable to search promotion as searching textbox did not display")
            for promotion in book_info["promotions"]:
                self.promotion_search_textbox.fill(promotion)
                self.promotion_checkbox.first.click()
            print(f"Selected promotion: {book_info['promotions']}")


    def add_new_book(self, book_info:dict):
        self.input_new_book_info(book_info)
        self.create_book_button.click()
    def edit_book_info(self, book_info:dict):
        # all infor ís optional
        if book_info.get("name"):
            self.book_name_field.fill(book_info["name"])
        if book_info.get("slug"):
            self.change_checkbox.click()
            self.slug_name_field.fill(book_info["slug"])
        if book_info.get("description"):
            self.description_field.fill(book_info["description"])
        if book_info.get("pictures"):
            upload_multiple_files(self.add_files,book_info["pictures"])
        if book_info.get("price"):
            self.price_field.fill(str(book_info["price"]))
        if book_info.get("categories"):
            select_multiple_dropdown_values(self.categories_dropdown, book_info["categories"])
        if book_info.get("promotions"):
            self.promotion_selection_icon.click()
            if not is_locator_visible(self.promotion_search_textbox):
                logger.warning(f"Unable to search promotion as searching textbox did not display")
            for promotion in book_info["promotions"]:
                self.promotion_search_textbox.fill(promotion)
                self.promotion_checkbox.first.click()
    def adjust_book_info(self, book_info:dict):
        self.edit_book_info(book_info)
        self.save_changes_button.click()

    def get_promotion_price(self, promotions):
        promotion_amount = 0
        self.promotion_selection_icon.click()
        if not is_locator_visible(self.promotion_search_textbox):
            logger.warning(f"Unable to search promotion as searching textbox did not display")
        for promotion in promotions:
            self.promotion_search_textbox.fill(promotion)
            if not is_locator_checked(self.promotion_checkbox):
                print("The searched promotion does not check successfully, please recheck")
                promotion_amount += self.get_column_texts_for_checked_rows("Value")
        return promotion_amount
    def get_promotions(self):
        self.promotion_selection_icon.click()
        if not is_locator_checked(self.promotion_checkbox):
            raise AssertionError ("The searched promotion does not check successfully, please recheck")
        return self.get_column_texts_for_checked_rows("CODE")
    def is_delete_popup_visible(self):
        return is_locator_visible(self.delete_title_popup)
    def is_delete_popup_invisible(self):
        return is_locator_invisible(self.delete_title_popup)
    def delete_book(self):
        self.delete_button.click()
        if not self.is_delete_popup_visible():
            raise AssertionError ("Not show the delete popup to confirm about deleting book, please recheck")
        self.confirm_delete_button.click()


























