from utils.generate_random_data_helper import random_bool, random_percentage_value, random_string

ALLOWED_CREATE_BOOK_PROMOTION_FIELDS = {"code","name","description","type","value","startDate",
                                        "endDate","isActive","books","configFe"}
ALLOWED_UPDATE_BOOK_PROMOTION_FIELDS = {"name","description","type","value","startDate",
                                        "endDate","isActive","books","configFe"}
ALLOWED_TYPE_VALUES = ["PERCENTAGE","FIXED_AMOUNT","FREE_SHIPPING"]

def create_book_promotion_payload(
    Json: dict | None = None,
    randomize_fields: list[str] | None = None,
    **overrides
):
    """
    :param Json: dict từ Json (optional)
    :param randomize_fields: list field muốn random (optional)
    :param overrides: field muốn override trực tiếp
    """

    invalid_fields = set(overrides.keys()) - ALLOWED_CREATE_BOOK_PROMOTION_FIELDS
    if invalid_fields:
        raise ValueError(f"Invalid fields in {invalid_fields}")
    # 🔹 Base mặc định
    payload = {
        "code": "PROMO_YVBFK",
        "name": "Local Price",
        "description": "abc",
        "type": "PERCENTAGE",
        "value": 25,
        "startDate": "2026-01-20T16:16:45.000Z",
        "endDate": "2026-02-05T16:16:45.000Z",
        "isActive": True,
        "books": [],
        "configFe": "",
    }

    # 🔹 Merge Excel
    if Json:
        payload.update(Json)

    # 🔹 Random theo field chỉ định
    if randomize_fields:
        for field in randomize_fields:
            if field == "isActive":
                payload["isActive"] = random_bool()
            elif field == "value":
                payload["value"] = random_percentage_value()
            elif field =="description":
                payload["description"] = random_string(min_length=6, max_length=50)
            elif field == "code":
                payload["code"] = random_string(prefix="PROMO_",upper_case=True,length=5)
    # 🔹 Override cuối cùng (ưu tiên cao nhất)
    payload.update(overrides)
    return payload
def update_book_promotion_payload(Json:dict|None= None,random_fields: list|list[str]=None,**overrides):
    invalid_fields = set(overrides.keys()) - ALLOWED_UPDATE_BOOK_PROMOTION_FIELDS
    if invalid_fields:
        raise ValueError(f"Invalid fields in {invalid_fields}")
    payload = {
        "name":"Local Price",
        "description":"Lisa updates this book promotion",
        "type":"PERCENTAGE",
        "value":20,
        "startDate":"2026-01-20T16:16:45.000Z",
        "endDate":"2026-02-05T16:16:45.000Z",
        "isActive":True,
        "books":[],
        "configFe":"",
    }
    if Json:
        payload.update(Json)
    if random_fields:
        for field in random_fields:
            if field == "isActive":
                payload["isActive"] = random_bool()
            if field == "value":
                payload["value"] = random_percentage_value()
            if field == "description":
                payload["description"] = random_string(min_length=6, max_length=50)
            if field == "code":
                payload["code"] = random_string(prefix="PROMO_",upper_case=True,length=5)

    payload.update(overrides)
    return payload

