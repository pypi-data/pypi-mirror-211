import json
import requests


class JSONner:
    @staticmethod
    def send_request(request_info):
        try:
            request = JSONner._build_request(request_info)
            response = requests.request(**request)
            return response
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    @staticmethod
    def _build_request(request_info):
        request_data = json.loads(request_info)
        method = request_data.get("method", "GET")
        url = request_data.get("url")
        headers = request_data.get("headers", {})
        params = request_data.get("params", {})
        data = request_data.get("data", {})
        auth = request_data.get("auth")

        request = {
            "method": method,
            "url": url,
            "headers": headers,
            "params": params,
            "data": data,
            "auth": auth,
        }

        return request
