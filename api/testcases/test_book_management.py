import logging

import pytest

from assertions.api_assertions import assert_status, assert_schema
from data.payloads.book_management_payload import register_book_payload,  \
    update_full_book_inf_payload
from api.schemas.book_management_schema import GET_BOOK_SCHEMA, GET_SPECIFIC_BOOK_SCHEMA
from api.schemas.error_schema import NORMAL_RESPONSE_SCHEMA
from api.services.book_management import BookManagement
from utils.json_helper import read_json_file
from utils.response_helper import get_response_data


logger = logging.getLogger(__name__)
invalid_data_json = read_json_file("data/json_data/Invalid_book_data.json")
valid_data_json = read_json_file("data/json_data/valid_book_data.json")

@pytest.mark.smoke
def test_get_book_list(authorized_client):
    book_management = BookManagement(authorized_client)
    response = book_management.get_book_list()
    data  = get_response_data(response)
    print("Body response: "+ str(data))
    assert_status(response, 200)
    assert_schema(response,GET_BOOK_SCHEMA)
    number_of_books = len(data["list"])
    assert number_of_books == data["pagination"]["lengthData"],f"current number of books show is {number_of_books} while actual length is {data['pagination']['lengthData']}"
    logger.info("Get book list successfully")

@pytest.mark.smoke
def test_create_and_view_new_book(authorized_client):
    book_management = BookManagement(authorized_client)
    book_id =""
    current_payload = register_book_payload(random_fields=["name","price","description","status","slug","categories"])
    book_slug = current_payload["slug"]
    book_name = current_payload["name"]
    book_description = current_payload["description"]
    book_status = current_payload["status"]
    book_price = current_payload["price"]
    book_categories = current_payload["categories"]
    print("Current body payload: " + str(current_payload))
    response = book_management.create_book(current_payload)
    data = get_response_data(response)
    print("Body response of creating book: " + str(data))
    assert_status(response, 200)
    assert_schema(response, NORMAL_RESPONSE_SCHEMA)
    assert "book created successfully" in data["msg"].lower()
    #Verify book after created
    book_list_response = book_management.get_book_list()
    book_list_data = get_response_data(book_list_response)
    assert_status(book_list_response, 200)
    for item in book_list_data["list"]:
        if item["name"] == book_name and item["slug"] == book_slug:
            book_id = item["id"]
            assert book_id !="", f"Actual book id is blank, pls recheck"
            break
    view_book_response = book_management.get_specific_book(book_id,"true")
    view_book_data = get_response_data(view_book_response)
    print("Body response of get specific book: " + str(view_book_data))
    assert_status(view_book_response, 200)
    assert book_price== view_book_data["price"],f"Actual book price is {view_book_data['price']} but actual price is {book_price}"
    assert book_status == view_book_data["status"],f"Actual book status is {view_book_data['status']} but actual status is {book_status}"
    assert book_description == view_book_data["description"],f"Actual description is {view_book_data['description']} but actual description is {book_description}"
    assert book_categories == view_book_data["categories"],f"Actual categories is {view_book_data['categories']} but actual categories is {book_categories}"
    logger.info(f"Create new book which {book_name} successfully")



def test_create_new_book_invalid_promotions(authorized_client):
    book_management = BookManagement(authorized_client)
    request_body = register_book_payload(name= "Linh Tinh",price=1500,status = "AVAILABLE",promotions=["bcc"],slug="belong to Lisa")
    print("Body request: " + str(request_body))
    response = book_management.create_book(request_body)
    data = get_response_data(response)
    print("Body response: " + str(data))
    assert_status(response, 404)
    assert_schema(response, NORMAL_RESPONSE_SCHEMA)
    assert "promotion not found" in data["msg"].lower()
    logger.info("Unable to create new book which promotion doesn't exist correctly")

@pytest.mark.parametrize("item", invalid_data_json)
def test_create_new_book_by_exist_book(authorized_client, item):
    book_management = BookManagement(authorized_client)
    current_payload = register_book_payload(Json=item,random_fields=["price","description","status","slug"])
    print("Body request: " + str(current_payload))
    response = book_management.create_book(current_payload)
    data = get_response_data(response)
    print("Body response: " + str(data))
    assert_status(response, 400)
    assert_schema(response, NORMAL_RESPONSE_SCHEMA)
    assert "book name already exists" in data["msg"].lower()
    logger.info("Unable to create new book which exist before correctly")

def test_view_specific_book(authorized_client):
    book_management = BookManagement(authorized_client)
    get_all_book_response = book_management.get_book_list()
    get_all_books_data = get_response_data(get_all_book_response)
    specific_book_id = get_all_books_data["list"][1]["id"]
    print("Specific book id: "+ str(specific_book_id))
    response = book_management.get_specific_book(specific_book_id,"true")
    data = get_response_data(response)
    print("Body response: " + str(data))
    assert_status(response, 200)
    assert_schema(
        response,
        GET_SPECIFIC_BOOK_SCHEMA
    )
    logger.info(f"View specific book which its id: {specific_book_id} successfully")

@pytest.mark.smoke
def test_update_specific_book_inf(authorized_client):
    # name = "Lisabbbb Nguyen"
    book_management = BookManagement(authorized_client)
    #Create book
    book_id = ""
    create_book_payload = register_book_payload(random_fields=["name","price", "description", "status", "slug","categories"])
    print("Current body payload for creating new book: " + str(create_book_payload))
    book_slug_before_update = create_book_payload["slug"]
    book_name_before_update = create_book_payload["name"]
    response = book_management.create_book(create_book_payload)
    # data = get_response_data(response)
    # print("Body response of creating new book: " + str(data))
    assert_status(response, 200)
    get_list_response = book_management.get_book_list()
    get_books_data = get_response_data(get_list_response)
    for item in get_books_data["list"]:
        if item["slug"] == book_slug_before_update and item["name"] == book_name_before_update:
            book_id = item["id"]
            assert book_id !="","Actual book id is blank,pls recheck"
            break

    #Update data
    current_payload = update_full_book_inf_payload(random_fields=["name","price", "description", "status", "slug","categories"])
    book_name = current_payload["name"]
    book_description = current_payload["description"]
    book_status = current_payload["status"]
    book_price = current_payload["price"]
    book_categories = current_payload["categories"]
    response = book_management.update_book(book_id,current_payload)
    data = get_response_data(response)
    # print("Body response: " + str(data))
    assert_status(response, 200)
    assert_schema(response,NORMAL_RESPONSE_SCHEMA)
    assert "book updated successfully" in data["msg"].lower()
#     Check this specific book after updated
    get_specific_book_response_after_updated = book_management.get_specific_book(book_id, "true")
    data_after = get_response_data(get_specific_book_response_after_updated)
    print("Body response of update book info: " + str(data_after))
    assert book_name == data_after["name"],f"Updated book name unsuccessfully, actual book name is {data_after['name']}"
    assert book_price == data_after["price"],f"Updated book price unsuccessfully, actual book price is {data_after['price']}"
    assert book_status == data_after["status"],f"Updated book status unsuccessfully, actual book status is {data_after['status']}"
    assert book_description == data_after["description"],f"Updated book description unsuccessfully, actual book description is {data_after['description']}"
    for cat in book_categories:
            assert cat in data_after["categories"], f"Missing category: {cat}"
    logger.info(f"Update book information of {book_name} which id - {book_id} correctly")

def test_update_exist_book_infor(authorized_client):
    name = ""
    book_management = BookManagement(authorized_client)
    get_all_book_response = book_management.get_book_list()
    get_all_books_data = get_response_data(get_all_book_response)
    specific_book_id = get_all_books_data["list"][1]["id"]
    print("Specific book id: " + str(specific_book_id))
    current_payload = update_full_book_inf_payload(name=name)
    response = book_management.update_book(specific_book_id,current_payload)
    print("Body request: " + str(current_payload))
    data = get_response_data(response)
    assert_status(response, 400)
    assert_schema(response,NORMAL_RESPONSE_SCHEMA)
    assert "book name already exists" in data["msg"].lower()
    logger.info("Unable to update book infor which already exist correctly")


def test_update_multiple_book_infor(authorized_client):
    name = "Manual documents 23"
    # description = "This book belongs to Lisa 123aaa"
    book_management = BookManagement(authorized_client)
    get_all_book_response = book_management.get_book_list()
    get_all_books_data = get_response_data(get_all_book_response)
    specific_book_id = get_all_books_data["list"][1]["id"]
    print("Specific book id: " + str(specific_book_id))
    current_payload = update_full_book_inf_payload(name=name)
    print("Body request: " + str(current_payload))
    response = book_management.update_book(specific_book_id,current_payload)
    data = get_response_data(response)
    assert_status(response, 200)
    assert_schema(response,NORMAL_RESPONSE_SCHEMA)
    assert "book updated successfully" in data["msg"].lower()
    #     Check this specific book after updated
    get_specific_book_response_after_updated = book_management.get_specific_book(specific_book_id, "true")
    data_after = get_response_data(get_specific_book_response_after_updated)
    print("Body response: " + str(data_after))
    assert name == data_after["name"], "Updated book name unsuccessfully"
    # assert description == data_after["description"], "Updated book description unsuccessfully"
    logger.info("Update multiple book information properly for specific book which their id: "+ {specific_book_id})

@pytest.mark.smoke
def test_delete_specific_book(authorized_client):
    book_management = BookManagement(authorized_client)
    # Create book
    book_id = ""
    create_book_payload = register_book_payload(
        random_fields=["name", "price", "description", "status", "slug", "categories"])
    print("Current body payload for creating new book: " + str(create_book_payload))
    book_slug = create_book_payload["slug"]
    book_name = create_book_payload["name"]
    response = book_management.create_book(create_book_payload)
    # data = get_response_data(response)
    # print("Body response of creating new book: " + str(data))
    assert_status(response, 200)
    get_list_response = book_management.get_book_list()
    get_books_data = get_response_data(get_list_response)
    for item in get_books_data["list"]:
        if item["slug"] == book_slug and item["name"] == book_name:
            book_id = item["id"]
            assert book_id != "", "Actual book id is blank,pls recheck"
            break
    print("Specific book id: " + str(book_id) + " its name - " + book_name )

    #Delete specific book
    response = book_management.delete_specific_book(book_id)
    data = get_response_data(response)
    print("Body response: " + str(data))
    assert_status(response, 200)
    assert_schema(response, NORMAL_RESPONSE_SCHEMA)
    assert "deleted successfully" in data["msg"].lower()

# Check after deleted this book
    get_specific_book_response = book_management.get_specific_book(book_id,"true")
    data_after = get_response_data(get_specific_book_response)
    print("Body response of delete api after deleted : " + str(data_after))
    assert_status(get_specific_book_response, 404)
    assert "book not found" in data_after["msg"].lower()
    logger.info("Delete specific book successfully which their id is: " + str(book_id) + " and their name is: " + str(book_name))

def test_delete_specific_book_by_invalid_book_id(authorized_client):
    book_management = BookManagement(authorized_client)
    response = book_management.delete_specific_book("")
    data = get_response_data(response)
    print("Body response: " + str(data))
    assert_status(response, 404)
    logger.info("Unable to delete a book by invalid id correctly")


def test_delete_specific_book_by_unexist_book_id(authorized_client):
    book_management = BookManagement(authorized_client)
    response = book_management.delete_specific_book("bbb")
    data = get_response_data(response)
    print("Body response: " + str(data))
    assert_status(response, 404)
    assert_schema(response, NORMAL_RESPONSE_SCHEMA)
    assert "book not found" in data["msg"].lower()
    logger.info("Unable to delete a book which unexist correctly")




