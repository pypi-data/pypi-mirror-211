import base64
class BasicAuth:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_auth_header(self):
        auth_header = f'Basic {base64.b64encode(f"{self.username}:{self.password}".encode()).decode()}'
        return {'Authorization': auth_header}


class TokenAuth:
    def __init__(self, token):
        self.token = token

    def get_auth_header(self):
        return {'Authorization': f'Token {self.token}'}
