from utils.generate_random_data_helper import random_string

ALLOWED_FIELDS_TO_CREATE_NEW_CATEGORY = {"name"}
ALLOWED_FIELDS_TO_UPDATE_CATEGORY = {"name","newName"}

def create_new_category_payload(random_field:list| None = None,**overrides):
    invalid_keys =  set(overrides.keys())-ALLOWED_FIELDS_TO_UPDATE_CATEGORY
    if invalid_keys:
        raise ValueError(f"Invalid keys in {invalid_keys}")
    payload = {
        "name":"Advertisement",
    }
    if random_field:
        if random_field == "name":
            payload["name"] = random_string(suffix=" added by Lisa", max_length= 6)
    payload.update(overrides)
    return payload

def update_category_payload(random_fields: list | None = None, **overrides):
    invalid_keys = set(overrides.keys()) - ALLOWED_FIELDS_TO_UPDATE_CATEGORY
    if invalid_keys:
        raise ValueError(f"Invalid keys in {invalid_keys}")

    payload = {
        "name": "Advertisement",
        "newName": "Adventure",
    }

    if random_fields:
        for random_field in random_fields:
            if random_field == "newName":
                payload["newName"] = random_string(suffix=" adjusted by Lisa", max_length=6)

    payload.update(overrides)
    return payload