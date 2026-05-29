import pytest

from assertions.api_assertions import assert_status, assert_schema
from data.payloads.book_promotion_payload import create_book_promotion_payload, update_book_promotion_payload
from api.schemas.book_promotion_schema import GET_BOOK_PROMOTION_LIST_SCHEMA, GET_SPECIFIC_BOOK_PROMOTION_SCHEMA
from api.schemas.error_schema import NORMAL_RESPONSE_SCHEMA, GET_422_ERROR_SCHEMA
from api.services.book_promotion import BookPromotion
from utils.json_helper import read_json_file
from utils.logger_helper import get_logger
from utils.response_helper import get_response_data


logger = get_logger(__name__)
json_data = read_json_file("data/json_data/promotion_data.json")
@pytest.mark.smoke
def test_get_book_promotion(authorized_client):
    book_promotion = BookPromotion(authorized_client)
    response = book_promotion.get_book_promotion_list()
    data = get_response_data(response)
    print("Response body: "+ str(data))
    assert_status(response, 200)
    assert_schema(response,GET_BOOK_PROMOTION_LIST_SCHEMA)
    total_promotion_no = len(data["list"])
    assert total_promotion_no == data["pagination"]["lengthData"],f"total of promotions is {total_promotion_no} while expected length is {data['pagination']['lengthData']}"
    logger.info("Get book promotion list successfully")

@pytest.mark.smoke
@pytest.mark.parametrize("item",json_data)
def test_get_specific_book_promotion_by_id(authorized_client,item):
    book_promotion = BookPromotion(authorized_client)
    book_promotion_id = ""
    # Create new book promotion
    current_payload = create_book_promotion_payload(Json=item,
                                                    randomize_fields=["code", "description", "value", "isActive"])
    print("Body request: " + str(current_payload))
    promotion_name = current_payload["name"]
    promotion_code = current_payload["code"]
    promotion_description = current_payload["description"]
    promotion_value = current_payload["value"]
    promotion_is_active = current_payload["isActive"]
    response = book_promotion.create_specific_promotion(current_payload)
    data = get_response_data(response)
    print("Response body: " + str(data))
    assert_status(response, 201)
    assert_schema(response, NORMAL_RESPONSE_SCHEMA)
    assert "created promotion successfully" in data["msg"].lower(), f"Actual response messenger is {data['msg']}"
    # Verify after created
    book_promotion_list_response = book_promotion.get_book_promotion_list()
    book_promotion_list_data = get_response_data(book_promotion_list_response)
    for item in book_promotion_list_data["list"]:
        if item["code"] == promotion_code and item["name"] == promotion_name:
            book_promotion_id = item["id"]
            assert book_promotion_id != "", f"Book promotion id is blank, pls check"
            break
    view_promotion_response = book_promotion.get_book_promotion_by_id(book_promotion_id)
    view_promotion_data = get_response_data(view_promotion_response)
    print("Response body of view specific promotion: "+ str(view_promotion_data))
    assert_status(view_promotion_response, 200)
    assert_schema(view_promotion_response,GET_SPECIFIC_BOOK_PROMOTION_SCHEMA)
    assert view_promotion_data["description"] == promotion_description,f"Actual description is {view_promotion_data['description']} while expected description is {promotion_description}"
    assert view_promotion_data["value"]==promotion_value,f"Actual promotion value is {view_promotion_data['value']} while expected value is {promotion_value}"
    assert view_promotion_data["isActive"] == promotion_is_active,f"Actual promotion status is {view_promotion_data['isActive']} while expected status is {promotion_is_active}"
    logger.info(f"Get specific book promotion which name - {promotion_name} successful")
def test_get_specific_book_promotion_with_unexist_id(authorized_client):
    book_promotion = BookPromotion(authorized_client)
    book_promotion_id = "cmn23wphs0ooq7uk1jabp5qmy999"
    response = book_promotion.get_book_promotion_by_id(book_promotion_id)
    data = get_response_data(response)
    print("Response body: "+ str(data))
    assert_status(response, 404)
    assert_schema(response,NORMAL_RESPONSE_SCHEMA)
    assert "promotion not found" in data["msg"].lower(), f"Actual response messenger is {data['message']}"
    logger.info("Can not get the specific book promotion with unexist id correctly")

@pytest.mark.smoke
@pytest.mark.parametrize("item",json_data)
def test_create_new_book_promotion(authorized_client,item):
    book_promotion = BookPromotion(authorized_client)
    book_promotion_id=""
    #Create new book promotion
    current_payload = create_book_promotion_payload(Json=item, randomize_fields=["code","description","value","isActive"])
    print("Body request: "+ str(current_payload))
    promotion_name = current_payload["name"]
    promotion_code = current_payload["code"]
    promotion_description = current_payload["description"]
    promotion_value = current_payload["value"]
    promotion_is_active = current_payload["isActive"]
    response = book_promotion.create_specific_promotion(current_payload)
    data = get_response_data(response)
    print("Response body: "+ str(data))
    assert_status(response, 201)
    assert_schema(response,NORMAL_RESPONSE_SCHEMA)
    assert "created promotion successfully" in data["msg"].lower(), f"Actual response messenger is {data['msg']}"
    #Verify after created
    book_promotion_list_response = book_promotion.get_book_promotion_list()
    book_promotion_list_data = get_response_data(book_promotion_list_response)
    for item in book_promotion_list_data["list"]:
        if item["code"] == promotion_code and item["name"] == promotion_name:
            assert item["description"] == promotion_description,f"actual description is {item['description']} while expected description is {promotion_description}"
            assert item["value"] == promotion_value,f"actual value is {item['value']} while expected value is {promotion_value}"
            assert item["isActive"] ==promotion_is_active,f"actual value is {item['isActive']} while expected value is {promotion_is_active}"
            book_promotion_id = item["id"]
            assert book_promotion_id != "", f"Book promotion id is blank, pls check"
            break
    logger.info(f"Create new book promotion which promotion id - {book_promotion_id}, promotion name - {promotion_name} and promotion code - {promotion_code} successful")

def test_create_exist_book_promotion_code(authorized_client):
    book_promotion = BookPromotion(authorized_client)
    current_payload = create_book_promotion_payload(name = "Test by Lisa 123")
    response = book_promotion.create_specific_promotion(current_payload)
    data = get_response_data(response)
    print("Response body: "+ str(data))
    assert_status(response, 422)
    assert_schema(response,GET_422_ERROR_SCHEMA)
    promotion_code = current_payload["code"]
    logger.info(f"Can not create new book promotion which exist promotion code - {promotion_code} correctly")

@pytest.mark.smoke
@pytest.mark.parametrize("item",json_data)
def test_delete_specific_book_promotion(authorized_client,item):
    book_promotion = BookPromotion(authorized_client)
    book_promotion_id=""
    #Create new book promotion
    current_payload = create_book_promotion_payload(Json=item,
                                                    randomize_fields=["code", "description", "value", "isActive"])
    book_promotion_code = current_payload["code"]
    print("Body request of create new promotion: " + str(current_payload))
    response = book_promotion.create_specific_promotion(current_payload)
    data = get_response_data(response)
    print("Response body of create new book promotion: " + str(data))
    assert_status(response, 201)
    #Get book promotion id which just created
    get_book_list_response = book_promotion.get_book_promotion_list()
    get_book_list_data = get_response_data(get_book_list_response)
    for item in get_book_list_data["list"]:
        if item["code"]== book_promotion_code:
            book_promotion_id = item["id"]
            break
    #Delete book by that id
    delete_promotion_response = book_promotion.delete_specific_promotion_by_id(book_promotion_id)
    delete_promotion_data = get_response_data(delete_promotion_response)
    assert_status(delete_promotion_response, 200)
    assert_schema(delete_promotion_response, NORMAL_RESPONSE_SCHEMA)
    print(f"Body response of delete request is: {str(delete_promotion_data)}")
    # Verify after deleted
    response_after_deleted = book_promotion.get_book_promotion_by_id(book_promotion_id)
    # data_after_deleted = get_response_data(response_after_deleted)
    assert_status(response_after_deleted, 404)
    print(f"Body response of get book promotion request is: {str(response_after_deleted)}")
    logger.info(f"Delete promotion which id - {book_promotion_id} successfully")

@pytest.mark.smoke
@pytest.mark.parametrize("item",json_data)
def test_update_book_promotion(authorized_client,item):
    book_promotion = BookPromotion(authorized_client)
    book_promotion_id = ""
    # Create new book promotion
    current_payload = create_book_promotion_payload(Json = item,
                                                    randomize_fields=["code", "description", "value", "isActive"])
    book_promotion_code = current_payload["code"]
    print("Body request of create new promotion: " + str(current_payload))
    response = book_promotion.create_specific_promotion(current_payload)
    data = get_response_data(response)
    print("Response body of create new book promotion: " + str(data))
    assert_status(response, 201)
    # Get book promotion id which just created
    get_book_list_response = book_promotion.get_book_promotion_list()
    get_book_list_data = get_response_data(get_book_list_response)
    for item in get_book_list_data["list"]:
        if item["code"] == book_promotion_code:
            book_promotion_id = item["id"]
            break
    #Update data
    payload = update_book_promotion_payload(Json=item,random_fields=["code","description","value","isActive"])
    print("Body request: "+ str(payload))
    updated_promotion_name = payload["name"]
    updated_promotion_code = payload["code"]
    updated_promotion_description = payload["description"]
    updated_promotion_value = payload["value"]
    updated_promotion_is_active = payload["isActive"]
    response = book_promotion.patch_specific_promotion_by_id(book_promotion_id,payload)
    data = get_response_data(response)
    print("Response body: "+ str(data))
    assert_status(response, 200)
    assert_schema(response,NORMAL_RESPONSE_SCHEMA)
    #Verify after update
    specific_promotion_response = book_promotion.get_book_promotion_by_id(book_promotion_id)
    specific_promotion_data = get_response_data(specific_promotion_response)
    assert updated_promotion_name == specific_promotion_data["name"],f"Update name unsuccessfully, actual promotion name is {specific_promotion_data["name"]}"
    assert updated_promotion_value==specific_promotion_data["value"]
    assert updated_promotion_is_active==specific_promotion_data["isActive"]
    assert updated_promotion_code==specific_promotion_data["code"]
    assert updated_promotion_description==specific_promotion_data["description"]
    logger.info(f"Update book promotion which promotion code is {book_promotion_id} and its new promotion name is {updated_promotion_name} successful")
def test_update_book_promotion_name_by_unexist_id(authorized_client):
    book_promotion = BookPromotion(authorized_client)
    book_promotion_id = ""
    updated_promotion_name = "Test by Lisa"
    payload = create_book_promotion_payload(name = updated_promotion_name)
    response = book_promotion.patch_specific_promotion_by_id(book_promotion_id,payload)
    data = get_response_data(response)
    print("Response body: "+ str(data))
    assert_status(response, 404)
    assert "NOT_FOUND".lower() in str(data).lower(),f"Actual response messenger is {data}"
    logger.info("Unable to update promotion name with unexist id correctly")




