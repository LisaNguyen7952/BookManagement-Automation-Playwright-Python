class BookPromotion:
    BASE_URL = "/api/promotion-book"
    def __init__(self,api_client):
        self.api_client = api_client
    def get_book_promotion_list(self):
        return self.api_client.get(f"{self.BASE_URL}")
    def get_book_promotion_by_id(self,id):
        return self.api_client.get(f"{self.BASE_URL}/{id}")
    def delete_specific_promotion_by_id(self,id):
        return self.api_client.delete(f"{self.BASE_URL}/{id}")
    def patch_specific_promotion_by_id(self,id,payload:dict):
        return self.api_client.patch(f"{self.BASE_URL}/{id}", json=payload)
    def create_specific_promotion(self,payload:dict):
        return self.api_client.post(f"{self.BASE_URL}", json=payload)
