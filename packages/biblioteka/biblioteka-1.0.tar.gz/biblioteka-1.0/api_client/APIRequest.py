import requests

class APIRequest:
    def __init__(self, url):
        self.url = url

    def send_request(self, method='GET', params=None, headers=None, data=None, timeout=None):
        response = requests.request(method, self.url, params=params, headers=headers, data=data, timeout=timeout)
        return response

    def get(self, params=None, headers=None, timeout=None):
        return self.send_request('GET', params=params, headers=headers, timeout=timeout)

    def post(self, data=None, headers=None, timeout=None):
        return self.send_request('POST', data=data, headers=headers, timeout=timeout)

    def put(self, data=None, headers=None, timeout=None):
        return self.send_request('PUT', data=data, headers=headers, timeout=timeout)

    def delete(self, params=None, headers=None, timeout=None):
        return self.send_request('DELETE', params=params, headers=headers, timeout=timeout)
