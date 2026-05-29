from assertions.api_assertions import assert_status, assert_schema
from api.schemas.file_management_schema import GET_FILES_SCHEMA
from api.services.file_management import FileManagement
from utils.response_helper import get_response_data


def test_upload_file(authorized_client):
    file_management = FileManagement(authorized_client)
    response = file_management.upload_file("/Users/mac/Downloads/test.doc","/")
    data = get_response_data(response)
    print("Response data: "+str(data))
    assert_status(response,200)

def test_get_file_list(authorized_client):
    file_management = FileManagement(authorized_client)
    response = file_management.get_file_list()
    data = get_response_data(response)
    print("Response data: "+str(data))
    assert_status(response,200)
    assert_schema(response,GET_FILES_SCHEMA)



