import requests
from licensespring.api.authorization import autorization_headers

from licensespring.api.error import ClientError
from licensespring.api.hardware import HardwareIdProvider
from licensespring.api.signature import verify_license_signature


class APIClient:
    def __init__(
        self,
        api_key,
        shared_key,
        hardware_id_provider=HardwareIdProvider,
        api_domain="api.licensespring.com",
        api_version="v4",
        verify_license_signature=True,
    ):
        self.api_key = api_key
        self.shared_key = shared_key

        self.hardware_id_provider = hardware_id_provider()

        self.api_base = "https://{}/api/{}".format(api_domain, api_version)

        self.verify_license_signature = verify_license_signature

    def api_url(self, endpoint):
        return "{}{}".format(self.api_base, endpoint)

    def request_headers(self, custom_headers={}):
        headers = {"Content-Type": "application/json"}
        authorization_headers = autorization_headers(self.api_key, self.shared_key)
        return {**headers, **authorization_headers, **custom_headers}

    def request_generic_data(
        self, product, hardware_id=None, license_key=None, username=None, password=None
    ):
        data = {
            "product": product,
            "hardware_id": hardware_id
            if hardware_id
            else self.hardware_id_provider.get_id(),
        }
        if license_key:
            data["license_key"] = license_key
        if username:
            data["username"] = username
        if password:
            data["password"] = password

        return data

    def request_additional_data(self, data, additional_data):
        for key, value in additional_data.items():
            if key is not None:
                data["key"] = value
        return data

    def send_request(self, method, endpoint, params=None, data=None):
        response = requests.request(
            method=method,
            url=self.api_url(endpoint),
            headers=self.request_headers(),
            params=params,
            json=data,
        )
        if 400 <= response.status_code < 500:
            raise ClientError(response)
        else:
            response.raise_for_status()
        return response

    def activate_license(
        self, product, hardware_id=None, license_key=None, username=None, password=None
    ):
        data = self.request_generic_data(
            product, hardware_id, license_key, username, password
        )

        response = self.send_request(
            method="post",
            endpoint="/activate_license",
            data=data,
        )
        response_json = response.json()

        if self.verify_license_signature:
            verify_license_signature(
                hardware_id,
                license_key,
                response_json.get("validity_period"),
                response_json.get("license_signature"),
            )

        return response_json

    def deactivate_license(
        self, product, hardware_id=None, license_key=None, username=None, password=None
    ):
        data = self.request_generic_data(
            product, hardware_id, license_key, username, password
        )

        response = self.send_request(
            method="post",
            endpoint="/deactivate_license",
            data=data,
        )
        return True if response.status_code == 200 else False

    def check_license(self, product, hardware_id=None, license_key=None, username=None):
        data = self.request_generic_data(
            product, hardware_id, license_key, username, None
        )
        response = self.send_request(
            method="get",
            endpoint="/check_license",
            params=data,
        )
        response_json = response.json()

        if self.verify_license_signature:
            verify_license_signature(
                hardware_id,
                license_key,
                response_json.get("validity_period"),
                response_json.get("license_signature"),
            )

        return response_json

    # TODO activate_offline

    # TODO deactivate_offline

    def add_consumption(
        self,
        product,
        hardware_id=None,
        license_key=None,
        username=None,
        password=None,
        consumptions=None,
        max_overages=None,
        allow_overages=None,
    ):

        data = self.request_generic_data(
            product, hardware_id, license_key, username, password
        )
        data = self.request_additional_data(
            data=data,
            additional_data={
                "consumptions": consumptions,
                "max_overages": max_overages,
                "allow_overages": allow_overages,
            },
        )

        response = self.send_request(
            method="post",
            endpoint="/add_consumption",
            json=data,
        )

        return response.json()

    def add_feature_consumption(
        self,
        product,
        hardware_id=None,
        license_key=None,
        username=None,
        password=None,
        feature=None,
        consumptions=None,
    ):

        data = self.request_generic_data(
            product, hardware_id, license_key, username, password
        )
        data["feature"] = feature
        data = self.request_additional_data(
            data=data,
            additional_data={
                "consumptions": consumptions,
            },
        )

        response = self.send_request(
            method="post",
            endpoint="/add_feature_consumption",
            json=data,
        )

        return response.json()

    def trial_key(
        self,
        product,
        hardware_id=None,
        email=None,
        license_policy=None,
        first_name=None,
        last_name=None,
        phone=None,
        address=None,
        postcode=None,
        state=None,
        country=None,
        city=None,
        reference=None,
    ):

        data = self.request_generic_data(product, hardware_id, None, None, None)
        data = self.request_additional_data(
            data=data,
            additional_data={
                "email": email,
                "license_policy": license_policy,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone,
                "address": address,
                "postcode": postcode,
                "state": state,
                "country": country,
                "city": city,
                "reference": reference,
            },
        )

        response = self.send_request(
            method="get",
            endpoint="/trial_key",
            json=data,
        )

        return response.json()

    def product_details(
        self,
        product,
    ):
        data = {"product": product}

        response = self.send_request(
            method="get",
            endpoint="/product_details",
            json=data,
        )

        return response.json()

    def track_device_variables(
        self,
        product,
        hardware_id=None,
        license_key=None,
        username=None,
        variables=None,
    ):

        data = self.request_generic_data(
            product, hardware_id, license_key, username, None
        )
        data["variables"] = variables

        response = self.send_request(
            method="post",
            endpoint="/track_device_variables",
            json=data,
        )

        return True if response.status_code == 200 else False

    def floating_release(
        self,
        product,
        hardware_id=None,
        license_key=None,
        username=None,
    ):

        data = self.request_generic_data(
            product, hardware_id, license_key, username, None
        )

        response = self.send_request(
            method="post",
            endpoint="/floating/release",
            json=data,
        )

        return True if response.status_code == 200 else False

    def floating_borrow(
        self,
        product,
        hardware_id=None,
        license_key=None,
        username=None,
        password=None,
        borrowed_until=None,
    ):

        data = self.request_generic_data(
            product, hardware_id, license_key, username, password
        )
        data["borrowed_until"] = borrowed_until

        response = self.send_request(
            method="post",
            endpoint="/floating/borrow",
            json=data,
        )

        return response.json()

    def change_password(self, username, password, new_password):
        data = {
            "username": username,
            "password": password,
            "new_password": new_password,
        }

        response = self.send_request(
            method="post",
            endpoint="/change_password",
            json=data,
        )

        return True if response.status_code == 200 else False

    def versions(
        self,
        product,
        hardware_id=None,
        license_key=None,
        username=None,
        env=None,
    ):

        data = self.request_generic_data(
            product, hardware_id, license_key, username, None
        )
        data = self.request_additional_data(
            data=data,
            additional_data={
                "env": env,
            },
        )

        response = self.send_request(
            method="get",
            endpoint="/versions",
            json=data,
        )

        return response.json()

    def installation_file(
        self,
        product,
        hardware_id=None,
        license_key=None,
        username=None,
        env=None,
        version=None,
    ):

        data = self.request_generic_data(
            product, hardware_id, license_key, username, None
        )
        data = self.request_additional_data(
            data=data,
            additional_data={
                "env": env,
                "version": version,
            },
        )

        response = self.send_request(
            method="get",
            endpoint="/installation_file",
            params=data,
        )

        return response.json()

    def customer_license_users(self, product, customer):
        data = {
            "product": product,
            "customer": customer,
        }

        response = self.send_request(
            method="get",
            endpoint="/customer_license_users",
            params=data,
        )

        return response.json()

    def sso_url(self, product, customer_account_code):
        data = {
            "product": product,
            "customer_account_code": customer_account_code,
        }

        response = self.send_request(
            method="get",
            endpoint="/sso_url",
            params=data,
        )

        return response.json()

    def get_device_variables(
        self,
        product,
        hardware_id=None,
        license_key=None,
        username=None,
    ):

        data = self.request_generic_data(
            product, hardware_id, license_key, username, None
        )

        response = self.send_request(
            method="get",
            endpoint="/get_device_variables",
            params=data,
        )

        return response.json()
