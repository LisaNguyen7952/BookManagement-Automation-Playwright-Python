


class UserInformation:
    BASE_PATH = "/api/me"
    # def __init__(self, authorized_client):
    #     self.authorized_client = authorized_client
    # def get_user_information(self):
    #     return self.authorized_client.get(f"{self.BASE_PATH}")

    def __init__(self,api_client):

        self.api = api_client
    def get_user_information(self, headers = None, params = None):
        return self.api.get(f"{self.BASE_PATH}",headers=headers,params=params)