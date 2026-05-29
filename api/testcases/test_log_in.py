# def test_log_in(authorized_client):
from assertions.api_assertions import assert_status, assert_schema
from api.schemas.login_schemas import LOGIN_SUCCESS_SCHEMA
from api.services.auth_service import AuthService


def test_login_success(api_client):
    login_service = AuthService(api_client)
    login_service.login(email="", password="")
    assert_status(login_service, 200)
    assert_schema(login_service, LOGIN_SUCCESS_SCHEMA)
