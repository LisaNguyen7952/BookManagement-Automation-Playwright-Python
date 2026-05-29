from random import seed

from assertions.ui_assertions import is_locator_visible, is_locator_invisible
from conftest import take_screenshot
from ui.pages.base_page import BasePage
from utils.interactions import get_locator_text, safe_click, safe_double_clicks
from utils.upload_helper import upload_multiple_files_one_by_one


class FileManagement(BasePage):
    def __init__(self,page):
        super().__init__(page)
        self.file_management_option = self.page.locator("//div[@class='simplebar-content']/nav/ul/li/a[.='File']")
        self.file_management_page_title = self.page.locator("h4", has_text="File Management")
        self.upload_file_button = self.page.locator("button", has_text="Upload file")
        self.upload_file_popup_title = self.page.locator("h2", has_text="Upload file")
        self.folder_textbox = self.page.locator("//textarea[@name='path']")
        self.upload_file_input = self.page.locator("//input[@name='file']")
        self.upload_button = self.page.get_by_role("button",name="Upload",exact=True)

        self.modify_icons = self.page.locator("//button[@type='button']")
        # self.modify_options = self.page.locator("//li[@role='menuitem']")
        self.rename_option = self.page.get_by_role("menuitem",name="Rename")
        self.copy_option = self.page.get_by_role("menuitem",name="Copy")
        self.delete_option = self.page.get_by_role("menuitem",name="Delete")
        self.move_option = self.page.get_by_role("menuitem",name="Move")
        self.popup_title = self.page.locator("h2")

        self.new_name_field = self.page.locator("//input[@name='name']")
        self.rename_button = self.page.locator("button",has_text="Rename")
        self.copy_button = self.page.locator("button",has_text="Copy")
        self.move_button = self.page.locator("button",has_text="Move")
        self.close_button = self.page.locator("button",has_text="Close")
        self.delete_button = self.page.locator("#dialog-delete-action")

        self.new_path_field = self.page.locator("//input[@role='combobox']")
        self.homepage_icon = self.page.locator("//li/button")
        self.folder_path = self.page.locator("//li/p")
        self.image_in_view = self.page.locator("//div[@role='dialog']//img")



    def uploaded_files_locator(self):
        return self.page.locator("//div[@role='button']")
    def get_uploaded_files(self):
        files =[]
        count = self.uploaded_files_locator().count()
        print(f"There are {count} uploaded files")
        for i in range(count):
            item_locator = self.uploaded_files_locator().nth(i)
            files.append({
                "name":get_locator_text(item_locator.locator("p")),
                "size":get_locator_text(item_locator.locator("span"))
            })
        return files

    def upload_files(self, files, folder_name:str|None
                     ):
        self.upload_file_button.click()
        if not is_locator_visible(self.upload_file_popup_title):
            raise Exception ("Not show the upload file popup, Can not upload file, pls check")
        if folder_name is not None:
            self.folder_textbox.fill(folder_name)
        upload_multiple_files_one_by_one(self.page, self.upload_file_input, files)
    def click_upload_files(self):
        self.upload_button.click()
    def is_upload_popup_invisible(self):
        return is_locator_invisible(self.upload_file_popup_title)
    def is_file_management_page_visible(self):
        return is_locator_visible(self.file_management_page_title)
    def navigate_to_file_management(self):
        self.file_management_option.click()

    def open_modify_popup_of_specific_file(self,column_name,key_search_by_name):
        specific_row = self.get_row_index_matching_condition(column_name, key_search_by_name)
        specific_row_locator = self.table_rows.nth(specific_row)
        modify_icon = specific_row_locator.locator("button")
        print(f"Number of modify button is {modify_icon.count()}")
        safe_click(modify_icon)

    def does_popup_close(self):
        return is_locator_invisible(self.popup_title)
    def does_popup_open(self):
        return is_locator_visible(self.popup_title)
    def move_file(self,new_path_file_name:str):
        self.move_option.click()
        if not self.does_popup_open():
            raise Exception ("Unable to open modify popup, pls check")
        self.new_path_field.fill(new_path_file_name)
        options = self.page.get_by_role("option")
        # print(f"Number of options is {options.count()}")
        # print(f"They are: {options.all_text_contents()}")
        options.first.click()
        self.move_button.click()
    def copy_file(self,new_path_file_name:str):
        self.copy_option.click()
        if not self.does_popup_open():
            raise Exception ("Unable to open modify popup, pls check")
        self.new_path_field.fill(new_path_file_name)
        options = self.page.get_by_role("option")
        options.first.click()
        self.copy_button.click()

    def rename_file(self,new_file_name:str):
        self.rename_option.click()
        if not self.does_popup_open():
            raise Exception ("Unable to open modify popup, pls check")
        self.new_name_field.fill(new_file_name)
        self.rename_button.click()

    def view_file(self, search_column_name, file_name):
        cell_file_locator = self.get_cell_locator(search_column_name, file_name)
        # file_type = (cell_file_locator.locator("img")).get_attribute("src")
        safe_double_clicks(cell_file_locator) #What ever file type, to view file, should double click
        if self.is_folder(cell_file_locator):
            raise ValueError(f"{file_name} is a folder")
        if not self.does_popup_open():
            raise Exception ("Unable to open review file popup, pls check")
        if not self.does_view_correct_file(file_name):
            raise AssertionError(f"View incorrect file {file_name}")
        self.close_button.click()
    def does_view_correct_file(self,file_name)->bool:
        file_name_path = self.image_in_view.get_attribute("src") or ""
        if file_name in file_name_path:
            return True
        else:
            print(f"Current file name path is {file_name_path}")
            return False
    def is_folder(self,item_locator)->bool:
        src = item_locator.locator("img").get_attribute("src")
        return "folder" in src.lower()
    def view_folder(self,search_column_name,folder_name):
        cell_file_locator = self.get_cell_locator(search_column_name, folder_name)
        # file_type = (cell_file_locator.locator("img")).get_attribute("src")
        if not self.is_folder(cell_file_locator):
            raise ValueError(f"Folder {folder_name} is not a folder")
        safe_double_clicks(cell_file_locator)
    def is_viewing_folder(self,folder_name)->bool:
        folder_path = get_locator_text(self.folder_path)
        return folder_name in folder_path






















