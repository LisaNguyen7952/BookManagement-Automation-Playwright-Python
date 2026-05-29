import datetime
import uuid


from utils.generate_random_data_helper import random_string, random_email, random_password, random_phone, \
    random_address, random_choice

#Validate structure of payload
ALLOWED_REGISTER_FIELDS = {"email", "name", "password", "phone", "address", "avatarUrl"}
ALLOWED_LOGIN_FIELDS = {"email", "password"}

#Tạo (POST) → thường có default + overrider(truyền giá trị khác)
def register_user_payload(Json:list| None = None,random_fields:list|None =None,**overrides):

    invalid_keys = set(overrides.keys()) - ALLOWED_REGISTER_FIELDS
    if invalid_keys:
        raise ValueError(f"Invalid fields: {invalid_keys}")

    payload = {
        "name": "Test User",
        "email": f"user_{uuid.uuid4().hex[:6]}@example.com", #auto generate email
        "password": "123456",
        "avatarUrl": "",
        "phone": "",
        "address": ""
    }
    if Json is not None:
        payload.update(Json)
    if random_fields:
        for random_field in random_fields:
            if random_field =="name":
                payload[
                    "name"] = f"{random_string(min_length=6, max_length=10, special=False, digits=False)} {random_string(min_length=6, max_length=10, special=False, digits=False)}"
            if random_field =="email":
                payload["email"] = random_email()
            if random_field =="password":
                payload["password"] = random_password()
            if random_field =="phone":
                payload["phone"] = random_phone()
            if random_field =="address":
                payload["address"] = random_address()
    payload.update(overrides)
    return payload
#Update (PATCH) → thường dùng None

def update_user_profile_payload(Json:list| None = None,random_fields:list|None=None,**overrides):
    payload = {
          "name": "",
          "email": "",
          "password": "",
          "avatarUrl": "",
          "address": "",
          "phone": "",
          "isActive": True
        }
    if Json is not None:
        payload.update(Json)
    if random_fields:
        for random_field in random_fields:
            if random_field =="name":
                payload["name"] = f"{random_string(min_length=6, max_length=10, special=False, digits=False)} {random_string(min_length=6, max_length=10, special=False, digits=False)}"
            if random_field =="email":
                payload["email"] = random_email()
            if random_field =="password":
                payload["password"] = random_password()
            if random_field =="phone":
                payload["phone"] = random_phone()
            if random_field =="address":
                payload["address"] = random_address()
            if random_field =="isActive":
                payload["isActive"] = random_choice([True, False])
    payload.update(overrides)
    return payload
def log_in_payload(**overrides):
    invalid_keys = set(overrides.keys()) - ALLOWED_LOGIN_FIELDS
    if invalid_keys:
        raise ValueError(f"Invalid fields: {invalid_keys}")
    payload = {}
    payload.update(overrides)
    return payload
ALLOWED_LOGIN_RESPONSE_FIELDS = {"msg", "accessToken", "exp"}

def log_in_response_payload(**overrides):
    invalid_keys = set(overrides.keys()) - ALLOWED_LOGIN_RESPONSE_FIELDS
    if invalid_keys:
        raise ValueError(f"Invalid fields: {invalid_keys}")
    payload = {
        "msg": "Login successfully",
        "accessToken": str(uuid.uuid4()),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    }
    payload.update(overrides)
    return payload

