import json
from json import JSONDecodeError
import time
from typing import Any, Dict

import allure



def get_json(response) -> Dict[str, Any]:
    try:
        return response.json()
    except JSONDecodeError as e:
        raise AssertionError(f"Invalid JSON response: {e}")

def assert_status(response, expected_status: int, payload=None):
    actual = response.status

    if actual != expected_status:

        # attach request payload nếu có
        if payload is not None:
            allure.attach(
                json.dumps(payload, indent=2),
                name="request_payload",
                attachment_type=allure.attachment_type.JSON
            )
            print("Request payload: "+ str(payload))

        # attach response body
        body = response.text()

        if body:
            allure.attach(
                body,
                name="response_body",
                attachment_type=allure.attachment_type.JSON
            )
            print("Response body: "+ str(body))
        else:
            allure.attach(
                "<EMPTY>",
                name="response_body",
                attachment_type=allure.attachment_type.TEXT
            )

        # attach status
        allure.attach(
            str(actual),
            name="actual_status",
            attachment_type=allure.attachment_type.TEXT
        )
        print("Actual status: "+ str(actual))

    assert actual == expected_status, \
        f"Expected {expected_status}, got {actual}"

def assert_response_time(
    start_time: float,
    max_ms: int
):
    elapsed = (time.time() - start_time) * 1000
    assert elapsed <= max_ms, (
        f"Response time {elapsed:.2f}ms exceeded {max_ms}ms"
    )

def log_response(response):
    print(f"\n[API DEBUG]")
    print(f"Status: {response.status}")
    print(f"Headers: {response.headers}")
    body = response.text()
    if body:
        print(f"Body: {body}")
from jsonschema import validate
from jsonschema.exceptions import ValidationError

def assert_schema(response, schema):
    body = get_json(response)

    try:
        validate(instance=body, schema=schema)
    except ValidationError as e:
        raise AssertionError(
            f"Schema validation failed:\n{e.message}"
        )

def find_data_by_key(data, key, value):
    if isinstance(data, list):
        for item in data:
            if item.get(key) == value:
                return item
        raise AssertionError(f"No item found with {key}={value}")

    elif isinstance(data, dict):
        if data.get(key) == value:
            return data
        raise AssertionError(f"Key {key} does not match {value}")

    else:
        raise TypeError("Unsupported data type")