class RegisterService:
    BASE_PATH = "/api/register"
    def __init__(self,api_client):
        self.api_client = api_client
    def register_user(self,payload:dict):
        return self.api_client.post(self.BASE_PATH,json=payload)

