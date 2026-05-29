
from assertions.ui_assertions import is_locator_visible, is_locator_invisible
from ui.pages.base_page import BasePage
from utils.interactions import safe_click, safe_fill, select_dropdown_value, get_locator_text, set_is_active
from utils.wait_helper import wait_for_table_stable


class UserManagementPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.page = page
        self.menu_icon = self.page.locator(".MuiButtonBase-root.MuiIconButton-root.MuiIconButton-sizeMedium.css-2j8huh")
        self.user_option = self.page.locator("li", has_text="User")
        self.user_management_title = self.page.locator("h4", has_text="User Management")
        self.add_new_user = self.page.locator("button", has_text="New User")
        self.user_popup_title = self.page.locator("h2",has_text="user")
        self.delete_user_popup_title = self.page.locator("h2",has_text="delete")
        self.upload_photo_icon = self.page.get_by_text("Upload Photo")
        self.name_field = self.page.locator("[name='name']")
        self.phone_field = self.page.locator("[name='phone']")
        self.division_drop_down = page.get_by_role("combobox", name="Division")
        self.division_input_field = self.page.locator("#address-division")
        # self.ward_drop_down = self.page.get_by_label("Ward")
        self.ward_input_field = self.page.locator("#address-ward")
        self.address_field = self.page.locator("#address")

        self.email_field = self.page.locator("//input[@name='email']")
        self.password_field = self.page.locator("//input[@name='password']")
        self.confirm_password_field = self.page.locator("//input[@name='password_confirmation']")
        self.active_toggle = self.page.locator("//input[@name='isActive']")
        self.save_button = self.page.get_by_text("Save")
        self.update_button = self.page.get_by_role("button",name="Update")


        self.search_textbox = self.page.get_by_placeholder("Search user (name, email, phone or address)")
        self.action_icon = self.page.locator("//td/button")
        self.adjust_option = self.page.locator("//li",has_text="Edit")
        self.delete_option = self.page.locator("//li", has_text="Delete")
        self.delete_button = self.page.locator("#dialog-delete-action")



    def navigate_to_user_management(self):
        self.user_option.click()

    def view_user_management(self):
       return is_locator_visible(self.user_management_title)

    def view_add_user_popup(self):
        safe_click(self.add_new_user)
        return is_locator_visible(self.user_popup_title)
    def open_user_adjustment_popup(self):
        self.action_icon.first.click()
        self.adjust_option.click()

    def view_user_popup(self):
        return is_locator_visible(self.user_popup_title)
    def does_user_popup_close(self):
        return is_locator_invisible(self.user_popup_title)

    def input_data_into_add_user_popup(self, user: dict):

        if "name" in user:
            safe_fill(self.name_field, user["name"])

        if "phone" in user:
            safe_fill(self.phone_field, user["phone"])

        if "division" in user:
            select_dropdown_value(self.division_drop_down, user["division"])

        if "ward" in user:
            safe_fill(self.ward_input_field, user["ward"])
            select_dropdown_value(self.ward_input_field, user["ward"])

        if "address" in user:
            safe_fill(self.address_field, user["address"])

        if "email" in user:
            safe_fill(self.email_field, user["email"])

        if "password" in user:
            safe_fill(self.password_field, user["password"])
            safe_fill(self.confirm_password_field, user["password"])

        if "isActive" in user:
            set_is_active(self.page, user["isActive"])


    def add_user(self,user:dict):
        self.input_data_into_add_user_popup(user)
        safe_click(self.save_button)

    def search_user(self,name):
        safe_fill(self.search_textbox,name)
        wait_for_table_stable(self.table_rows)


    def get_number_of_users(self):
        return self.get_number_of_records()
    def are_search_results_matching(self, key_search):
        search_by_columns = ["name", "phone", "address"]
        return self.get_number_record_and_verify_search_results(key_search,search_by_columns)
    # def view_update_user_popup(self):


    def get_user_info(self):
        user_name = get_locator_text(self.name_field)
        user_phone = get_locator_text(self.phone_field)
        user_address = get_locator_text(self.address_field)
        user_email = get_locator_text(self.email_field)
        # user_password = get_locator_text(self.password_field)
        user_division = get_locator_text(self.division_drop_down)
        user_ward = get_locator_text(self.ward_input_field)
        if self.active_toggle.is_checked():
            user_is_active = True
        else:
            user_is_active = False
        user={
            "name":user_name,
            "phone":user_phone,
            "address":user_address,
            "email":user_email,
            "division":user_division,
            "ward":user_ward,
            "isActive":user_is_active
        }
        return user

    def edit_user_info(self, user: dict):
        if "name" in user:
            safe_fill(self.name_field, user["name"])

        if "phone" in user:
            safe_fill(self.phone_field, user["phone"])

        if "division" in user:
            select_dropdown_value(self.division_drop_down, user["division"])

        if "ward" in user:
            select_dropdown_value(self.ward_input_field,user.get("ward"))

        if "address" in user:
            safe_fill(self.address_field, user["address"])

        if "email" in user:
            safe_fill(self.email_field, user["email"])

        if "password" in user:
            safe_fill(self.password_field, user["password"])
            safe_fill(self.confirm_password_field, user["password"])

        if "isActive" in user:
            set_is_active(self.page, user["isActive"])


    def update_user_info(self,user:dict):
        self.edit_user_info(user)
        self.update_button.click()
    def open_user_delete_popup(self):
        self.action_icon.first.click()
        self.delete_option.click()
    def does_delete_confirmation_popup_open(self):
        return is_locator_visible(self.delete_user_popup_title)

    def does_delete_confirmation_popup_close(self):
        return is_locator_visible(self.delete_user_popup_title)
    def delete_specific_user(self):
        self.delete_button.click()













