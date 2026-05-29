import pytest

from assertions.api_assertions import assert_status, assert_schema
from conftest import authorized_client
from data.payloads.authenticator_payload import register_user_payload
from api.schemas.register_schema import REGISTER_4XX_SCHEMA, REGISTER_SUCCESS_SCHEMA
from api.services.register_service import RegisterService
from api.services.user_management import UserManagement
from data.user_factory import UserFactory
from utils.logger_helper import get_logger
from utils.response_helper import get_response_data

logger = get_logger()
def test_register_user_missing_email(api_client):
    register_service = RegisterService(api_client)
    # current_payload = register_user_payload(email=None)
    current_payload = UserFactory.create(email=None)
    response = register_service.register_user(current_payload)
    # assert response.status_code == 200
    assert_status(response, 422)
    assert_schema(response,REGISTER_4XX_SCHEMA)
    # logger.info("Refer to payload request: "+ str(current_payload))
    # logger.info("Refer to payload response: "+ response.text())
    logger.info("Unable to create user without email correctly")

def test_register_user_mising_name(api_client):
    register_service = RegisterService(api_client)
    current_payload = UserFactory.create(name=None)
    response = register_service.register_user(current_payload)
    # assert response.status_code == 200
    assert_status(response, 422)
    assert_schema(response, REGISTER_4XX_SCHEMA)
    print("Refer to payload request: "+ str(current_payload))
    # print("Refer to payload response: "+ str(response))
    logger.info("Unable to create user without name correctly")

def test_register_user_exist_user(api_client):
    register_service = RegisterService(api_client)
    current_payload = register_user_payload(email="lisa.nguyenpro@outlook.com", name="Lisa")
    response = register_service.register_user(current_payload)
    logger.info("Refer to payload request: " + str(current_payload))
    # assert response.status_code == 200
    assert_status(response, 422)
    assert_schema(response, REGISTER_4XX_SCHEMA)
    # logger.info("Refer to payload response: "+ str(response))
    logger.info("Unable to create user by existing email correctly")

@pytest.mark.smoke
def test_register_user(authorized_client):
    register_service = RegisterService(authorized_client)
    # current_payload = register_user_payload(random_fields=["email", "name","phone","address","password"])
    current_payload = UserFactory.create(random_fields=["email", "name", "phone", "address", "password"])
    print("Refer to payload request: " + str(current_payload))
    user_email = current_payload["email"]
    user_name = current_payload["name"]
    user_phone = current_payload["phone"]
    user_address = current_payload["address"]
    # user_password = current_payload["password"]
    created_user_response = register_service.register_user(current_payload)
    # created_user_data = get_response_data(created_user_response)
    assert_status(created_user_response, 201)
    assert_schema(created_user_response,REGISTER_SUCCESS_SCHEMA)
    print("Refer to payload response: "+ str(created_user_response))
    #Verify the new user
    user_id =""
    user_information = UserManagement(authorized_client)
    get_all_users_response = user_information.get_all_users()
    assert_status(get_all_users_response, 200)
    get_all_users_data = get_response_data(get_all_users_response)
    for user in get_all_users_data["list"]:
        if user["email"]==user_email and user["name"]==user_name:
            user_id = user["id"]
            assert user_id != "","User id is still blank"
            break
    get_user_information_response = user_information.get_user_by_id(user_id)
    assert_status(get_user_information_response, 200)
    get_user_info_data = get_response_data(get_user_information_response)
    assert get_user_info_data["email"] == user_email,f"Actual email is {get_user_info_data['email']}, not {user_email}"
    assert get_user_info_data["name"] == user_name,f"Actual name is {get_user_info_data['name']}, not {user_name}"
    assert get_user_info_data["phone"] == user_phone,f"Actual phone is {get_user_info_data['phone']}, not {user_phone}"
    assert get_user_info_data["address"] == user_address,f"Actual address is {get_user_info_data['address']}, not {user_address}"
    logger.info(f"Create new user which name - {user_name} and email - {user_email} successfully")


