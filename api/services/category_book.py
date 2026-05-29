class BookCategories:
    BASE_URL = "/api/category-book"

    def __init__(self,api_client):
        self.api_client = api_client

    def get_category_list(self):
        return self.api_client.get(f"{self.BASE_URL}")
    def create_new_category(self,payload:dict):
        return self.api_client.post(f"{self.BASE_URL}", json=payload)
    def update_category(self,payload:dict):
        return self.api_client.put(f"{self.BASE_URL}", json=payload)
    def delete_specific_category(self,category_name):
        return self.api_client.delete(f"{self.BASE_URL}/{category_name}")