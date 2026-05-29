import uuid

from utils.generate_random_data_helper import random_string, random_email, random_password, random_phone, \
    random_address, random_city, random_choice


class UserFactory:
    @staticmethod
    def create(
        json: dict | None = None,
        random_fields: list | None = None,
        **overrides
    ):
        payload = {
            "name": "Lisa Lee",
            "email": f"user_{uuid.uuid4().hex[:6]}@example.com",
            "password": "123456!",
            "phone": "0901220099",
            "address": "Address default by Lisa",
            "division": "Lào Cai",
            "ward": "Xã Tú Lệ",
            "isActive": True
        }

        if json:
            payload.update(json)

        if random_fields:
            for field in random_fields:
                if field == "name":
                    payload["name"] = f"{random_string(6,10)} {random_string(6,10)}"
                elif field == "email":
                    payload["email"] = random_email()
                elif field == "password":
                    payload["password"] = random_password()
                elif field == "phone":
                    payload["phone"] = random_phone()
                elif field == "address":
                    payload["address"] = random_address()
                elif field == "division":
                    payload["division"] = random_city()
                elif field == "isActive":
                    payload["isActive"] = random_choice([True, False])

        payload.update(overrides)
        return payload
    @staticmethod
    def update(
            Json: dict | None = None,
            random_fields: list | None = None,
            **overrides
    ):
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
                if random_field == "name":
                    payload[
                        "name"] = f"{random_string(min_length=6, max_length=10, special=False, digits=False)} {random_string(min_length=6, max_length=10, special=False, digits=False)}"
                if random_field == "email":
                    payload["email"] = random_email()
                if random_field == "password":
                    payload["password"] = random_password()
                if random_field == "phone":
                    payload["phone"] = random_phone()
                if random_field == "address":
                    payload["address"] = random_address()
                if random_field == "isActive":
                    payload["isActive"] = random_choice([True, False])
        payload.update(overrides)
        return payload
