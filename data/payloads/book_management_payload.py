
from utils.generate_random_data_helper import random_price, random_availability_value, random_string, random_choice

ALLOWED_CREATE_NEW_BOOK_FIELDS = {"categories","name","price","status","description","pictures",
                                  "promotions","slug"}

ALLOWED_STATUS = ["AVAILABLE","UNAVAILABLE"]
ALLOWED_CATEGORIES = ["Adventure","Story","Blogger","Last Minute","Early Book","PROMO_2gG1y"]
#Tạo (POST) → thường có default + overrider(truyền giá trị khác)
def register_book_payload(
        Json:dict|None= None,
        random_fields:list|None= None,
        **overrides):

    invalid_keys = set(overrides.keys()) - ALLOWED_CREATE_NEW_BOOK_FIELDS
    if invalid_keys:
        raise ValueError(f"Invalid fields: {invalid_keys}")

    payload = {
        "name": "Harry Porter",
        "price": 13000,
        "status": "AVAILABLE",
        "description": "This book belongs to Lisa",
        "pictures": ["No pictures"],
        "promotions": [],
        "slug": "abcmkl",
        "categories": ["Adventure"],
    }
    if Json:
        payload.update(Json)
    if random_fields:
        for random_field in random_fields:
            if random_field == "name":
                payload["name"] = random_string(suffix=" book",length=10,)
            if random_field == "price":
                payload["price"] = random_price()
            if random_field == "description":
                payload["description"] = random_string(max_length=30)
            if random_field == "status":
                payload["status"] = random_availability_value()
            if random_field =="slug":
                payload["slug"] = random_string(length=6)
            if random_field == "categories":
                payload["categories"] = [random_choice(ALLOWED_CATEGORIES)]

    payload.update(overrides)
    return payload
# def register_book_payload(**overrides):
#
#     invalid_keys = set(overrides.keys()) - ALLOWED_CREATE_NEW_BOOK_FIELDS
#     if invalid_keys:
#         raise ValueError(f"Invalid fields: {invalid_keys}")
#
#     payload = {
#         "name": "Harry Porter",
#         "price": 13000,
#         "status": "AVAILABLE",
#         "description": "This book belongs to Lisa",
#         "pictures": ["No pictures"],
#         "promotions": [],
#         "slug": "i-dont-know-slug",
#         "categories": ["Adventure"],
#     }
#     payload.update(overrides)
#     if payload["status"] not in ALLOWED_STATUS:
#         raise ValueError(f"Invalid status: {payload['status']}")
#     if not isinstance(payload["promotions"], list):
#         raise TypeError("promotions must be a list")
#     return payload
ALLOWED_UPDATE_BOOK_FIELDS = {
    "name","slug","description","status","pictures","categories","price","promotions"
}


def update_full_book_inf_payload(
        Json:dict|None= None,
        random_fields:list|None= None,
        **overrides):
    invalid_keys = set(overrides.keys()) - ALLOWED_UPDATE_BOOK_FIELDS
    if invalid_keys:
        raise ValueError(f"Invalid fields: {invalid_keys}")
    payload = {
        "name": "Harry Porter99",
        "slug": "abc1234",
        "description": "This book belongs to Lisa",
        "status": "AVAILABLE",
        "pictures": [],
        "categories": ["Adventure"],
        "promotions": [],
        "price": 13000,

    }
    if Json:
        payload.update(Json)
    if random_fields:
        for random_field in random_fields:
            if random_field == "name":
                payload["name"] = random_string(suffix=" book",length=10,)
            if random_field == "price":
                payload["price"] = random_price()
            if random_field == "description":
                payload["description"] = random_string(max_length=30)
            if random_field == "status":
                payload["status"] = random_availability_value()
            if random_field == "slug":
                payload["slug"] = random_string(length=6)
            if random_field == "categories":
                payload["categories"] = [random_choice(ALLOWED_CATEGORIES)]
    payload.update(overrides)
    return payload
