from assertions.ui_assertions import assert_list_dict_match
from ui.pages.file_management import FileManagement
from utils.logger_helper import logger
from utils.upload_helper import  get_values_from_list_dict


def test_upload_file(page):
    file_management = FileManagement(page)
    folder_name =""
    document_files = [{'name': '616194573_3384053701750492_4966226566346009925_n.jpg', 'size': '105.0 KB - jpeg'},
                      {'name': 'VJ703_13-01-2026.png', 'size': '155.5 KB - png'}]
    upload_file_names = get_values_from_list_dict(document_files, "name")
    print(f"upload_file_names: {upload_file_names}")
    file_management.navigate_to_file_management()
    assert file_management.is_file_management_page_visible(),f"Unable to view file management page, pls check"
    number_of_records_before_adding = file_management.get_number_of_records()
    file_management.upload_files(upload_file_names,folder_name)
    uploaded_files = file_management.get_uploaded_files()
    print(f"Refer to the uploaded files info: {uploaded_files}")
    assert_list_dict_match(uploaded_files,document_files),f"Not matching uploaded files, pls check"
    file_management.click_upload_files()
    assert file_management.is_upload_popup_invisible(),f"Unable to close upload popup after clicking on the upload button, pls check"
    #Verify uploaded files
    number_of_records_after_added = file_management.get_number_of_records()
    assert number_of_records_after_added == number_of_records_before_adding + len(upload_file_names)
def test_upload_existing_files(page):
    file_management = FileManagement(page)
    folder_name =""
    document_files = [{'name': '616194573_3384053701750492_4966226566346009925_n.jpg', 'size': '105.0 KB - jpeg'},
                      {'name': 'VJ703_13-01-2026.png', 'size': '155.5 KB - png'}]
    upload_file_names = get_values_from_list_dict(document_files, "name")
    print(f"upload_file_names: {upload_file_names}")
    file_management.navigate_to_file_management()
    assert file_management.is_file_management_page_visible(), f"Unable to view file management page, pls check"
    # number_of_records_before_adding = file_management.get_number_of_records()
    file_management.upload_files(upload_file_names, folder_name)
    uploaded_files = file_management.get_uploaded_files()
    print(f"Refer to the uploaded files info: {uploaded_files}")
    file_management.click_upload_files()
    alert = file_management.get_alert_text()
    print(f"Refer to the alert info: {alert}")
    if not alert:
        logger.warning("Not show any alert, pls check")
    assert "file already exist" in alert.lower(),f"Actual {alert}"
    logger.info(f"Unable to exist upload files {document_files}")
def test_move_file(page):
    file_name = "abc.png"
    new_path_file ="Demo"
    file_management = FileManagement(page)
    file_management.navigate_to_file_management()
    file_management.search_data(file_name)
    number_of_files = file_management.get_number_of_records()
    assert number_of_files>0,f"Unable to move file as no uploaded files, pls check"
    file_management.open_modify_popup_of_specific_file("Name",file_name)
    file_management.move_file(new_path_file)
    assert file_management.does_popup_close(), f"Unable to close modify popup, pls check"
    #Verify after moving file
    file_management.search_data(file_name)
    number_of_files_after_moving = file_management.get_number_of_records()
    assert number_of_files_after_moving == number_of_files -1,f"Moving file unsuccessfully, number of records after moving file is {number_of_files_after_moving} while before it is {number_of_files} pls check"
    logger.info(f"Moving file {file_name} to new path {new_path_file} correctly")

def test_rename_file(page):
    file_management = FileManagement(page)
    file_name = "Adjusted_by_Lisa"
    new_file_name = "Adjusted_by_Lisa.png"
    file_management.navigate_to_file_management()
    file_management.search_data(new_file_name)
    number_of_new_name_files_before_rename = file_management.get_number_of_records()
    assert number_of_new_name_files_before_rename == 0,f"Unable to rename file {file_name} as new name - {new_file_name} is exist, pls check"
    file_management.search_data(file_name)
    number_of_files_before_rename = file_management.get_number_of_records()
    assert number_of_files_before_rename !=0,f"Unable to rename file {file_name} as this file is not exist, pls check"
    file_management.search_data(file_name)
    file_management.open_modify_popup_of_specific_file("Name",file_name)
    file_management.rename_file(new_file_name)
    assert file_management.does_popup_close(), f"Unable to close modify popup, pls check"
    #Verify rename action
    file_management.search_data(new_file_name)
    number_of_new_name_files_after_rename = file_management.get_number_of_records()
    assert number_of_new_name_files_after_rename !=0,f"Rename unsuccessfully as number of new name file after rename is {number_of_new_name_files_after_rename}, pls check"
    logger.info(f"Rename file {file_name} to new name {new_file_name} correctly")


def test_copy_file(page):
    file_management = FileManagement(page)
    file_name = "Adjusted_by_Lisa.png"
    new_file_path = "Demo"
    file_management.navigate_to_file_management()
    file_management.search_data(new_file_path)
    assert file_management.get_number_of_records()!=0,f"Unable to copy file {new_file_path} as this file is not exist, pls check"
    file_management.search_data(file_name)
    number_of_files = file_management.get_number_of_records()
    assert number_of_files != 0, f"Unable to copy file to new path {new_file_path} as no file name {file_name} pls check"
    file_management.open_modify_popup_of_specific_file("Name",file_name)
    file_management.rename_file(new_file_path)
    assert file_management.does_popup_close(), f"Unable to close modify popup, pls check"
    #Verify
    file_management.search_data(new_file_path)

def test_view_file(page):
    file_management = FileManagement(page)
    file_name = "Adjusted_by_Lisa.png"
    file_management.navigate_to_file_management()
    file_management.search_data(file_name)
    number_of_files = file_management.get_number_of_records()
    if number_of_files == 0:
        raise AssertionError(f"No file name - {file_name} to view file, pls check")

    file_management.view_file("Name",file_name)
    assert file_management.does_popup_close(), f"Unable to close popup, pls check"
    logger.info(f"View file name - {file_name} properly")
def test_view_folder(page):
    file_management = FileManagement(page)
    file_name = "Demo"
    file_management.navigate_to_file_management()
    file_management.search_data(file_name)
    number_of_files = file_management.get_number_of_records()
    if number_of_files == 0:
        raise AssertionError(f"No folder name - {file_name} to view, pls check")
    file_management.view_folder("Name",file_name)
    logger.info(f"Refer to list file on this folder - {file_management.get_list_of_records('Name')} properly")
    logger.info(f"View folder name - {file_name} properly")
def test_view_specific_file_in_folder(page):
    file_management = FileManagement(page)
    file_name = "456539411_10162315187151995_350653124633702597_n.jpg"
    folder_name = "Demo"
    file_management.navigate_to_file_management()
    file_management.search_data(folder_name)
    number_of_files = file_management.get_number_of_records()
    if number_of_files == 0:
        raise AssertionError(f"No folder name - {file_name} to view, pls check")
    file_management.view_folder("Name",folder_name)
    list_of_files = file_management.get_list_of_records('Name')
    assert file_name in list_of_files, f"{file_name} is not in the list - {list_of_files}"
    file_management.view_file("Name",file_name)
    logger.info(f"View specific file - {file_name} in the specific folder - {folder_name} properly")

















