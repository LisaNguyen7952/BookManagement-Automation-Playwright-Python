from assertions.ui_assertions import assert_dict_match
from data.user_factory import UserFactory
from ui.pages.user_management import UserManagementPage
from utils.logger_helper import logger


def test_view_user_management(page):
    user_management = UserManagementPage(page)
    user_management.navigate_to_user_management()
    assert user_management.view_user_management(),f"Unable to view user management page, pls recheck"
    print ("Number of row in the user table "+ str(user_management.get_table_rows()))
    print ("Number of column in the user table "+ str(user_management.get_table_columns()))

def test_search_users(page):
    key_search ="anc"
    user_management = UserManagementPage(page)
    user_management.navigate_to_user_management()
    assert user_management.view_user_management()
    user_management.search_user(key_search)
    number_of_users = user_management.get_number_of_users()
    logger.info(f"Number of users : {number_of_users} which matching key-search - {key_search}")


def test_search_users_and_verify_search_data(page):
    key_search ="lisa@gmail.com"
    user_management = UserManagementPage(page)
    user_management.navigate_to_user_management()
    assert user_management.view_user_management()
    user_management.search_user(key_search)
    assert user_management.are_search_results_matching(key_search), f"Some records does not match - {key_search}"
    logger.info(f"All search results matching key-search - {key_search} correctly")

def test_add_user(page):
    user = {
        "name": "Lisa",
        "phone": "0901009911",
        "division": "Lào Cai",
        "ward": "Xã Tú Lệ",
        "address": "15 Lê Đình Lý, Tú Lệ, Lào Cai",
        "email": "lisa7@gmail.com",
        "password": "123456@",

    }
    user_management = UserManagementPage(page)
    user_management.navigate_to_user_management()
    assert user_management.view_user_management(),f"Unable to view user management page, pls recheck"
    #Check number of users which name = "" before adding
    user_management.search_user(user["email"])
    number_of_users_before_add = user_management.get_number_of_users()
    assert user_management.view_add_user_popup(),f"Unable to view add user pop up, pls recheck"
    user_management.add_user(user)
    #verify after added user
    user_management.search_user(user["email"])
    number_of_users_after_add = user_management.get_number_of_users()
    assert number_of_users_after_add == number_of_users_before_add + 1,f"Number of users which have email - {user["email"]} after add is {number_of_users_after_add} and before add is {number_of_users_before_add}"
    logger.info(f"Create new user - {user["name"]} successfully")

def test_add_user_by_random_data(page):
    user_management = UserManagementPage(page)
    user_management.navigate_to_user_management()
    assert user_management.view_user_management(),f"Unable to view user management page, pls recheck"
    user=UserFactory.create(random_fields=["name","phone","address","password","email","isActive"])
    print(f"Refer to data of test data: {str(user)}")
    # Check number of users which name = "" before adding
    user_management.search_user(user["email"])
    number_of_users_before_add = user_management.get_number_of_users()
    assert user_management.view_add_user_popup(), f"Unable to view add user pop up, pls recheck"
    user_management.add_user(user)
    # verify after added user
    user_management.search_user(user["email"])
    number_of_users_after_add = user_management.get_number_of_users()
    assert number_of_users_after_add == number_of_users_before_add + 1, f"Number of users which have email - {user["email"]} after add is {number_of_users_after_add} and before add is {number_of_users_before_add}"
    logger.info(f"Create new user - {user["name"]} successfully")
    #verify data
    user_management.open_user_adjustment_popup()
    assert user_management.view_user_popup(),f"Unable to view user detail pop up, pls recheck"
    current_user_infor = user_management.get_user_info()
    assert current_user_infor["name"] == user["name"],f"Actual name is {current_user_infor['name']} and expected name is {user['name']}"
    assert current_user_infor["email"] == user["email"],f"Actual email is {current_user_infor['email']} and expected email is {user['email']}"
    assert current_user_infor["address"] == user["address"],f"Actual address is {current_user_infor['address']} and expected address is {user['address']}"
    assert current_user_infor["phone"] == user["phone"],f"Actual phone is {current_user_infor['phone']}"
    assert current_user_infor["isActive"] == user["isActive"],f"Actual isActive is {current_user_infor['isActive']} and expected isActive is {user['isActive']}"
    logger.info(f"All data of new user - {user["name"]} which email - {user["email"]} show successfully")

def test_view_user_data(page):
    user_management = UserManagementPage(page)
    user_management.navigate_to_user_management()
    assert user_management.view_user_management(), f"Unable to view user management page, pls recheck"
    # user = UserFactory.create(random_fields=["name", "phone", "address", "password", "email", "isActive"])
    user = {'name': 'MmjSRk huJ2ad', 'email': 'oieq3706u@yahoo.com', 'password': 'pJrlYonI!', 'phone': '0350939338', 'address': '339 Tran Hung Dao, Lào Cai', 'division': 'Lào Cai', 'ward': 'Xã Tú Lệ', 'isActive': True}
    print(f"Refer to data of test data: {str(user)}")
    #Search by email
    user_management.search_user(user["email"])
    user_management.open_user_adjustment_popup()
    assert user_management.view_user_popup(), f"Unable to view user detail pop up, pls recheck"
    current_user_infor = user_management.get_user_info()
    print(f"Refer to current user data: {str(current_user_infor)}")
    assert current_user_infor["name"] == user[
        "name"], f"Actual name is {current_user_infor['name']} and expected name is {user['name']}"
    assert current_user_infor["email"] == user[
        "email"], f"Actual email is {current_user_infor['email']} and expected email is {user['email']}"
    assert current_user_infor["address"] == user[
        "address"], f"Actual address is {current_user_infor['address']} and expected address is {user['address']}"
    assert current_user_infor["phone"] == user["phone"], f"Actual phone is {current_user_infor['phone']}"
    assert current_user_infor["isActive"] == user[
        "isActive"], f"Actual isActive is {current_user_infor['isActive']} and expected isActive is {user['isActive']}"
    logger.info(f"All data of user - {user["name"]} which email - {user["email"]} show successfully")


def test_adjust_fully_user_info_by_email(page):
    user={
        'name': 'Lisa newest',
        'email': 'oieq3706u@yahoo.com',
        'password': 'pJrlYonI!',
        'phone': '0905111111',
        'address': '111 Tran Hung Dao, Lào Cai',
        'division': 'Lào Cai',
        'ward': 'Xã Tú Lệ',
        'isActive': False
    }
    user_management = UserManagementPage(page)
    user_management.navigate_to_user_management()
    # Search by email
    user_management.search_user(user["email"])
    if user_management.get_number_of_users()==0:
        logger.warning(f"No users found, pls recheck")
    user_management.open_user_adjustment_popup()
    assert user_management.view_user_popup(), f"Unable to view user detail pop up, pls recheck"
    #Update user info
    user_management.update_user_info(user)
    assert user_management.does_user_popup_close(),f"Unable to close user detail popup after adjusted information"
    #Verify
    user_management.open_user_adjustment_popup()
    assert user_management.view_user_popup(), f"Unable to view user detail pop up, pls recheck"
    current_user_infor = user_management.get_user_info()
    print(f"Refer to current user data: {str(current_user_infor)}")
    assert_dict_match(current_user_infor, user,ignore_keys=["password"])
    logger.info(f"All data of user which email - {user["email"]} show successfully after updated")

def test_update_partially_user_data_by_email(page):
    user = {
        'name': 'Updated by lisa 3rd',
        'email': 'oieq3706u@yahoo.com',
        'phone': '0909000000',
        'isActive': False
    }
    user_management = UserManagementPage(page)
    user_management.navigate_to_user_management()
    # Search by email
    user_management.search_user(user["email"])
    if user_management.get_number_of_users() == 0:
        logger.warning(f"No users found to adjust, pls recheck")
    user_management.open_user_adjustment_popup()
    assert user_management.view_user_popup(), f"Unable to view user detail pop up, pls recheck"
    # Update user info
    user_management.update_user_info(user)
    assert user_management.does_user_popup_close(),f"Unable to close user detail popup after adjusted information"
    # Verify
    user_management.open_user_adjustment_popup()
    assert user_management.view_user_popup(), f"Unable to view user detail pop up, pls recheck"
    current_user_infor = user_management.get_user_info()
    print(f"Refer to current user data: {str(current_user_infor)}")
    assert_dict_match(current_user_infor, user)
    logger.info(f"All new data of user which email - {user["email"]} show successfully")


def test_delete_user_by_email(page):
    user_management = UserManagementPage(page)
    user_email = "lisa7@gmail.com"
    #searching specific user by email
    user_management.navigate_to_user_management()
    user_management.search_user(user_email)
    if user_management.get_number_of_users() == 0:
        logger.warning(f"No users found, unable to delete user, pls recheck")
    number_of_users_before_deleted = user_management.get_number_of_users()
    #delete user
    user_management.open_user_delete_popup()
    assert user_management.does_delete_confirmation_popup_open(),f"Unable to open the delete confirmation"
    user_management.delete_specific_user()
    assert user_management.does_delete_confirmation_popup_close(),f"Unable to close the delete confirmation"
    number_of_users_after_deleted = user_management.get_number_of_users()

    assert (number_of_users_after_deleted == number_of_users_before_deleted
            - 1),f"number of user before deleted is {number_of_users_before_deleted} after deleted is {number_of_users_after_deleted}"
    logger.info(f"user which email - {user_email} delete successfully")





