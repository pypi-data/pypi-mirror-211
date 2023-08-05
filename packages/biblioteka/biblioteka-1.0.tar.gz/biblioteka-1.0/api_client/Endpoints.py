from api_client.APIRequest import APIRequest
from api_client.APIResponse import APIResponse


class UserEndpoint:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_user(self, user_id):
        url = f'{self.base_url}/users/{user_id}'
        request = APIRequest(url)
        response = request.send_request()
        return APIResponse(response)


class PostEndpoint:
    def __init__(self, base_url):
        self.base_url = base_url

    def create_post(self, data):
        url = f'{self.base_url}/posts'
        request = APIRequest(url)
        response = request.send_request(method='POST', data=data)
        return APIResponse(response)
