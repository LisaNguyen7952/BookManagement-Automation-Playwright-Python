import logging

import pytest

from assertions.api_assertions import assert_status, assert_schema
from data.payloads.authenticator_payload import register_user_payload
from api.schemas.error_schema import NORMAL_RESPONSE_SCHEMA
from api.schemas.get_user_schema import GET_USER_INFOR_SUCCESS_SCHEMA, GET_USER_LIST_SUCCESS_SCHEMA
from api.services.register_service import RegisterService
from api.services.user_information import UserInformation
from api.services.user_management import UserManagement
from utils.response_helper import get_response_data

logger = logging.getLogger(__name__)

def test_get_user_infor(authorized_client,config_data):
    get_user_infor = UserInformation(authorized_client)
    response = get_user_infor.get_user_information()
    assert_status(response, 200)
    assert_schema(response, GET_USER_INFOR_SUCCESS_SCHEMA)
    data = response.json()
    assert data["email"]== config_data["email"]


def test_get_user_inf_incorrect_header(api_client):
    get_user_infor = UserInformation(api_client)
    response = get_user_infor.get_user_information(headers = "")
    assert_status(response,401)
    assert_schema(response, NORMAL_RESPONSE_SCHEMA)
    data = get_response_data(response)
    logger.info("Body response: "+ str(data))
    assert "invalid authorization" in str(data).lower()

def test_get_user_list(authorized_client):
    get_user_list = UserManagement(authorized_client)
    response = get_user_list.get_all_users()
    assert_status(response, 200)
    assert_schema(response,GET_USER_LIST_SUCCESS_SCHEMA)
    data = response.json()
    print("Body response: "+ str(data))
    user_in_total = data["pagination"]["total"]
    current_page = data["pagination"]["currentPage"]
    number_of_pages = data["pagination"]["totalPage"]
    length_of_page = data["pagination"]["lengthData"]
    if current_page != number_of_pages:
        assert current_page ==1, f"current default page is {current_page} instead of 1st"
        assert length_of_page ==10
    logger.info("Show the default page is 1st page and Number of page record is 10 correctly")
    logger.info("Current page is "+ str(data["pagination"]["currentPage"]) + "/" + str(data["pagination"]["totalPage"]))
    logger.info(f"Get list of users properly and in total: {user_in_total}")


def test_get_specific_user(authorized_client):
    get_specific_user = UserManagement(authorized_client)
    response_api_1 = get_specific_user.get_all_users()
    assert_status(response_api_1, 200)
    data_api_1 = response_api_1.json()
    user_id = data_api_1["list"][0]["id"]
    response = get_specific_user.get_user_by_id(user_id)
    assert_status(response, 200)
    assert_schema(response, GET_USER_INFOR_SUCCESS_SCHEMA)
    data = response.json()
    logger.info("Body response: "+ str(data))

def test_get_specific_user_unexist_user_id(authorized_client):
    get_specific_user = UserManagement(authorized_client)
    response = get_specific_user.get_user_by_id("1")
    assert_status(response, 404)
    assert_schema(response, NORMAL_RESPONSE_SCHEMA)
    data = response.json()
    print("Body response: "+ str(data))
    assert "user not found" in str(data).lower()

def test_get_specific_user_blank_user_id(authorized_client):
    get_specific_user = UserManagement(authorized_client)
    response = get_specific_user.get_user_by_id("")
    assert_status(response, 200)
    # assert_schema(response, GET_OTHER_ERROR_SCHEMA)
    data = response.json()
    print("Body response: "+ str(data))

def test_get_specific_user_invalid_user_ids(authorized_client):
    get_specific_user = UserManagement(authorized_client)
    response = get_specific_user.get_user_by_id("%^&*")
    assert_status(response, 400)
    # assert_schema(response, GET_OTHER_ERROR_SCHEMA)
    data = get_response_data(response)
    print("Body response: "+ str(data))
    assert "bad request" in str(data).lower()

def test_delete_specific_user(authorized_client):
    get_specific_user = UserManagement(authorized_client)
    response_api_1 = get_specific_user.get_all_users()
    assert_status(response_api_1, 200)
    data_api_1 = response_api_1.json()
    user_id = data_api_1["list"][0]["id"]
    user_name = data_api_1["list"][0]["name"]
    response = get_specific_user.delete_user_by_id(user_id)
    assert_status(response,200)
    # assert_schema(response,)
    data = response.json()
    print("Body response: " + str(data))
    assert "deleted successfully" in str(data).lower()
    logger.info("Delete successfully specific user id: "+ str(user_id) + "name: "+ str(user_name))

@pytest.mark.smoke
def test_delete_user_by_email(authorized_client):
    register_service = RegisterService(authorized_client)
    current_payload = register_user_payload( name="Lisa")
    user_email = current_payload["email"]
    response = register_service.register_user(current_payload)
    logger.info("Refer to payload request: " + str(current_payload))
    assert_status(response, 201)
    #Get user id
    get_specific_user = UserManagement(authorized_client)
    response_api_1 = get_specific_user.get_all_users()
    assert_status(response_api_1, 200)
    data_api_1 = get_response_data(response_api_1)
    user_id =""
    for item in data_api_1["list"]:
        if item["email"] == user_email:
            user_id = item["id"]
            assert user_id != "","User id is still blank"
            break
    #Delete by that id
    user_management = UserManagement(authorized_client)
    delete_user_response = user_management.delete_user_by_id(user_id)
    assert_status(delete_user_response, 200)
    #Verify this delete job
    get_specific_user_response = user_management.get_user_by_id(user_id)
    assert_status(get_specific_user_response, 404)
    logger.info("Delete user by email: "+ f"{user_email} successfully")


def test_delete_user_blank_user_id(authorized_client):
    get_specific_user = UserManagement(authorized_client)
    response = get_specific_user.delete_user_by_id("")
    assert_status(response, 404)
    data = get_response_data(response)
    logger.info("Body response: "+ str(data))
    assert "not_found" in data.lower()

def test_delete_specific_user_invalid_user_id(authorized_client):
    get_specific_user = UserManagement(authorized_client)
    response = get_specific_user.delete_user_by_id("$%^&")
    assert_status(response, 400)
    data = get_response_data(response)
    logger.info("Can not delete_user_blank_user_id refer to body response: "+ str(data))
    assert "bad request" in str(data).lower()

def test_delete_specific_user_unexist_user_id(authorized_client):
    get_specific_user = UserManagement(authorized_client)
    response = get_specific_user.delete_user_by_id("1")
    assert_status(response, 404)
    assert_schema(response, NORMAL_RESPONSE_SCHEMA)
    data = get_response_data(response)
    logger.info("Body response: "+ str(data))
    assert "not found" in str(data).lower()