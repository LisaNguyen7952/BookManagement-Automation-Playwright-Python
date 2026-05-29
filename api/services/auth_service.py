class AuthService:
    BASE_PATH="api/login"
    def __init__(self, api_client):
        self.api_client = api_client
    # def login(self, username, password):
    #     payload = {"username": username, "password": password}
    #     response = self.api_client.post(self.BASE_PATH, json=payload)
    #     assert response.status_code == 200
    #     data = response.json()
    #     token = data["accessToken"]
    #     exp_token = data["exp"]
    #     print("Current access token:", token)
    #     print("Current expiration token:", exp_token)
    #     return token
    def login(self, email, password):
        payload = {"email": email, "password": password}
        return self.api_client.post(self.BASE_PATH, json=payload)