import requests
from licensespring.api.authorization import autorization_headers

from licensespring.api.error import HTTPClientError
from licensespring.api.hardware import HardwareIdProvider


class APIClient:
    def __init__(
        self,
        api_key,
        shared_key,
        hardware_id_provider=HardwareIdProvider,
        api_domain="api.licensespring.com",
        api_version="v4",
    ):
        self.api_key = api_key
        self.shared_key = shared_key

        self.hardware_id_provider = hardware_id_provider()

        self.api_base = "https://{}/api/{}".format(api_domain, api_version)

    def api_url(self, endpoint):
        return "{}{}".format(self.api_base, endpoint)

    def request_headers(self, custom_headers={}):
        headers = {"Content-Type": "application/json"}
        authorization_headers = autorization_headers(self.api_key, self.shared_key)
        return {**headers, **authorization_headers, **custom_headers}

    def send_request(self, method, endpoint, params=None, data=None):
        response = requests.request(
            method=method,
            url=self.api_url(endpoint),
            headers=self.request_headers(),
            params=params,
            json=data,
        )
        if 400 <= response.status_code < 500:
            raise HTTPClientError(response)
        else:
            response.raise_for_status()
        return response

    def activate_license(self, product, hardware_id=None, license_key=None):
        response = self.send_request(
            method="post",
            endpoint="/activate_license",
            data={
                "product": product,
                "hardware_id": hardware_id
                if hardware_id
                else self.hardware_id_provider.get_id(),
                "license_key": license_key,
            },
        )
        return response.json()

    def deactivate_license(self, product, hardware_id=None, license_key=None):
        response = self.send_request(
            method="post",
            endpoint="/deactivate_license",
            data={
                "product": product,
                "hardware_id": hardware_id
                if hardware_id
                else self.hardware_id_provider.get_id(),
                "license_key": license_key,
            },
        )
        return True if response.status_code == 200 else False

    def check_license(self, product, hardware_id=None, license_key=None):
        response = self.send_request(
            method="get",
            endpoint="/check_license",
            params={
                "product": product,
                "hardware_id": hardware_id
                if hardware_id
                else self.hardware_id_provider.get_id(),
                "license_key": license_key,
            },
        )
        return response.json()
