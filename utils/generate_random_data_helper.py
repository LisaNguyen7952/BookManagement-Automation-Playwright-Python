

import random
import string


import random
import string
import uuid


def random_string(
    length: int | None = None,
    min_length: int = 6,
    max_length: int = 12,
    prefix: str = "",
    suffix: str = "",
    upper_case: bool = True,
    lower_case: bool = True,
    digits: bool = True,
    special: bool = False,
    custom_chars: str | None = None
):
    """
    Generate random string with flexible length and charset
    """

    # 🔹 Xác định độ dài
    if length is None:
        length = random.randint(min_length, max_length)

    # 🔹 Xác định charset
    if custom_chars:
        chars = custom_chars
    else:
        chars = ""
        if upper_case:
            chars += string.ascii_uppercase
        if lower_case:
            chars += string.ascii_lowercase
        if digits:
            chars += string.digits
        if special:
            chars += "!@#$%^&*"

    if not chars:
        raise ValueError("At least one character set must be selected")

    # 🔹 Generate
    random_part = ''.join(random.choices(chars, k=length))

    return f"{prefix}{random_part}{suffix}"

def random_price():
    return random.randint(1000, 1000000)
def random_bool():
    return random.choice([True, False])
def random_percentage_value():
    return random.randint (0, 100)
def random_availability_value():
    return random.choice(["AVAILABLE", "UNAVAILABLE"])
def random_choice(options: list):
    if not options:
        raise ValueError("Options list can not be empty")
    return random.choice(options)
def random_email():
    first = random_string(
        special=False,
        min_length=6,
        max_length=10,
        upper_case=False,
        digits=True
    )
    domain = random.choice(["gmail.com", "yahoo.com", "example.com"])
    return f"{first}@{domain}"


def random_phone():
    prefix = random.choice(["032", "033", "034", "035", "036", "037", "038", "039",
                            "070", "076", "077", "078", "079",
                            "081", "082", "083", "084", "085",
                            "056", "058"])
    number = ''.join(random.choices(string.digits, k=7))
    return prefix + number
def random_address():
    street_num = random.randint(1, 999)
    street_name = random.choice([
        "Nguyen Trai", "Le Loi", "Tran Hung Dao", "Pham Van Dong"
    ])
    city = random.choice(["Đà Nẵng","Lào Cai", "Hồ Chí Minh"])
    return f"{street_num} {street_name}, {city}"
def random_city():
    return random.choice([
        "Đà Nẵng","Lào Cai", "Hồ Chí Minh"
    ])

def random_password():
    return random_string(
        min_length=8,
        max_length=12,
        upper_case=True,
        lower_case=True,
        digits=True,
        special=True
    )
def random_item_list_from_list(data_list: list, min_items=1, max_items=2) -> list:
    count = random.randint(min_items, min(max_items, len(data_list)))
    return random.sample(data_list, count)
