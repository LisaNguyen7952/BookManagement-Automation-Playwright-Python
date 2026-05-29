
from configs.env_config import BOOK_CATEGORY_LIST, PROMOTION_LIST, PICTURE_LIST
from utils.generate_random_data_helper import random_string, random_price, random_item_list_from_list


class BookFactory:
    @staticmethod
    def create_book(
            Json:dict| None = None,
            random_fields: list| None = None,
            **overrides
    ):
        payload = {
            "name": "Lisa 's adventure",
            "price": 860418,
            "description": "09Li707rRoFkR",
            "pictures": ["616194573_3384053701750492_4966226566346009925_n.jpg"],
            "promotions": [],
            "categories": ['Adventure', 'Advertisement']

        }
        if Json:
            payload.update(Json)
        if random_fields:
            for field in random_fields:
                if field == "name":
                    payload["name"] = f"{random_string(max_length=10, digits=False,special=False, custom_chars=False)} {random_string(max_length=10, digits=False,special=False, custom_chars=False)}"
                if field == "price":
                    payload["price"] = random_price()
                if field == "description":
                    payload["description"] = random_string(max_length=20,digits=False,special=False,custom_chars=False)
                if field == "categories":
                    payload["categories"] = random_item_list_from_list(BOOK_CATEGORY_LIST,1,2)
                if field == "promotions":
                    payload["promotions"] = random_item_list_from_list(PROMOTION_LIST,0,3)
                if field == "slug":
                    payload["slug"] = random_string(length=6)
                if field == "pictures":
                    payload["pictures"] = random_item_list_from_list(PICTURE_LIST,1,2)

        payload.update(overrides)
        return payload
