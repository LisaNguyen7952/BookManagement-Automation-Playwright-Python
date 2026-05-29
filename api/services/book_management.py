class BookManagement:
    BASE_URL = "/api/book"
    def __init__(self,api_client):
        self.api_client = api_client

    def get_book_list(self):
        return self.api_client.get(self.BASE_URL)
    def create_book(self,payload:dict):
        return self.api_client.post(self.BASE_URL,json =payload)
    def get_specific_book(self, book_id, view_mode:bool = True):
        return self.api_client.get(f"{self.BASE_URL}/{book_id}?view={view_mode}")
    def update_book(self, book_id, payload:dict):
        return self.api_client.patch(f"{self.BASE_URL}/{book_id}", json=payload)
    def delete_specific_book(self, book_id):
        return self.api_client.delete(f"{self.BASE_URL}/{book_id}")