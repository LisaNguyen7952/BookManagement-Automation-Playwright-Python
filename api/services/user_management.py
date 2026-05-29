


class UserManagement:
    BASE_PATH = "/api/user"
    def __init__(self,api_client):
        self.api = api_client

    def get_all_users(self):
        return self.api.get(self.BASE_PATH)
    def get_user_by_id(self,user_id):
        return self.api.get(f"{self.BASE_PATH}/{user_id}")
    def create_new_user(self,payload:dict):
        return self.api.post(self.BASE_PATH,json=payload)
    def update_user_by_id(self,user_id,payload:dict):
        return self.api.patch(f"{self.BASE_PATH}/{user_id}",json=payload)
    def delete_user_by_id(self, user_id):
        return self.api.delete(f"{self.BASE_PATH}/{user_id}")