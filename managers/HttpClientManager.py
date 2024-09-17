import requests

class HTTPClientManager:
    def __init__(self, base_url):
        self.base_url = base_url

    def _handle_response(self, response):
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"Error {response.status_code}: {response.text}")

    def get(self, endpoint, headers=None, params=None):
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.get(url, headers=headers, params=params)
            return self._handle_response(response)
        except Exception as e:
            print(f"GET request failed: {e}")

    def post(self, endpoint, headers=None, data=None):
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.post(url, headers=headers, json=data)
            return self._handle_response(response)
        except Exception as e:
            print(f"POST request failed: {e}")

    def put(self, endpoint, headers=None, data=None):
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.put(url, headers=headers, json=data)
            return self._handle_response(response)
        except Exception as e:
            print(f"PUT request failed: {e}")

    def delete(self, endpoint, headers=None):
        try:
            url = f"{self.base_url}/{endpoint}"
            response = requests.delete(url, headers=headers)
            return self._handle_response(response)
        except Exception as e:
            print(f"DELETE request failed: {e}")