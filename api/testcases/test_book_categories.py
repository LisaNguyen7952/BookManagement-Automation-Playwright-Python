import pytest

from assertions.api_assertions import assert_status, assert_schema
from data.payloads.book_categoryies_payload import create_new_category_payload, update_category_payload
from api.schemas.book_category_schema import GET_BOOK_CATEGORY_LIST_SCHEMA
from api.schemas.error_schema import NORMAL_RESPONSE_SCHEMA
from api.services.category_book import BookCategories
from utils.logger_helper import get_logger
from utils.response_helper import get_response_data

logger = get_logger(__name__)
def test_get_book_categories(authorized_client):
    book_categories = BookCategories(authorized_client)
    response = book_categories.get_category_list()
    data = get_response_data(response)
    print("Body response: " + str(data))
    assert_status(response, 200)
    assert_schema(response,GET_BOOK_CATEGORY_LIST_SCHEMA)
    category_no = len(data["list"])
    assert category_no == data["pagination"]["total"],"incorrect number of book categories"
    logger.info(f"Get the book categories properly and total is {category_no}")

def test_create_new_book_category(authorized_client):
    book_categories = BookCategories(authorized_client)
    created_categories_payload = create_new_category_payload(random_field="name")
    print("Body request of created categories : " + str(created_categories_payload))
    book_category_name = created_categories_payload["name"]
    response = book_categories.create_new_category(created_categories_payload)
    data = get_response_data(response)
    print("Body response of created categories: " + str(data))
    assert_status(response, 201)
    assert_schema(response,NORMAL_RESPONSE_SCHEMA)
    #Verify after created
    current_response_of_book_category_list = book_categories.get_category_list()
    current_data_of_book_category_list = get_response_data(current_response_of_book_category_list)
    current_category_names = [item["name"] for item in current_data_of_book_category_list["list"]]
    assert book_category_name in current_category_names, f"{book_category_name} is created unsuccessfully"
    logger.info(f"Create new book category - {book_category_name} successfully")

@pytest.mark.smoke
def test_update_and_view_book_category(authorized_client):
    book_categories = BookCategories(authorized_client)
    created_categories_payload = create_new_category_payload(random_field="name")
    print("Body request of created categories : " + str(created_categories_payload))
    book_category_name = created_categories_payload["name"]
    response = book_categories.create_new_category(created_categories_payload)
    data = get_response_data(response)
    print("Body response of created categories: " + str(data))
    assert_status(response, 201)
    assert_schema(response, NORMAL_RESPONSE_SCHEMA)
    #update categories
    updated_categories_payload = update_category_payload(name = book_category_name,random_fields=["newName"])
    updated_category_name = updated_categories_payload["newName"]
    print("Body request of updated categories: " + str(updated_categories_payload))
    updated_category_response = book_categories.update_category(updated_categories_payload)
    updated_category_data = get_response_data(updated_category_response)
    print("Body response of updated categories: " + str(updated_category_data))
    assert_status(updated_category_response, 200)
    #Verify categories
    category_list_response = book_categories.get_category_list()
    category_list_data = get_response_data(category_list_response)
    print("Body response of list categories: " + str(category_list_data))
    category_name_list = [item["name"] for item in category_list_data["list"]]
    assert updated_category_name in category_name_list, f"{book_category_name} is updated unsuccessfully"
    assert book_category_name not in category_name_list, f"{book_category_name} is updated unsuccessfully"
    logger.info(f"Create and Update book category - {book_category_name} to new category - {updated_category_name} successfully")





def test_create_new_book_category_with_blank_name(authorized_client):
    book_categories = BookCategories(authorized_client)
    response = book_categories.create_new_category(create_new_category_payload(name =""))
    data = get_response_data(response)
    print("Body response: " + str(data))
    assert_status(response, 400)
    assert_schema(response,NORMAL_RESPONSE_SCHEMA)
    logger.info("Unable to create new book category with blank name correctly")

def test_create_new_book_category_with_exist_name(authorized_client):
    book_categories = BookCategories(authorized_client)
    response = book_categories.create_new_category(create_new_category_payload(name ="Novel"))
    data = get_response_data(response)
    print("Body response: " + str(data))
    assert_status(response, 400)
    assert_schema(response,NORMAL_RESPONSE_SCHEMA)
    assert "category already exists" in data["msg"].lower(),"return incorrect messenger"
    logger.info("Unable to create new book category with existing name correctly")

@pytest.mark.smoke
def test_delete_book_category(authorized_client):
    book_categories = BookCategories(authorized_client)
    created_categories_payload = create_new_category_payload(random_field="name")
    print("Body request of created categories : " + str(created_categories_payload))
    book_category_name = created_categories_payload["name"]
    response = book_categories.create_new_category(created_categories_payload)
    data = get_response_data(response)
    print("Body response of created categories: " + str(data))
    assert_status(response, 201)
    assert_schema(response, NORMAL_RESPONSE_SCHEMA)
    #Delete category
    response = book_categories.delete_specific_category(book_category_name)
    data = get_response_data(response)
    print("Body response of deleted request: " + str(data))
    assert_status(response, 200)
    assert_schema(response, NORMAL_RESPONSE_SCHEMA)
    # Verify after delete
    current_response_of_book_category_list = book_categories.get_category_list()
    current_data_of_book_category_list = get_response_data(current_response_of_book_category_list)
    current_category_names = [item["name"].strip().lower() for item in current_data_of_book_category_list["list"]]
    assert book_category_name.strip().lower() not in current_category_names, f"{book_category_name} is deleted unsuccessfully"
    logger.info(f"Create and Delete book category - {book_category_name} successfully")

