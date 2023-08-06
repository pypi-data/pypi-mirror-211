import requests
from urllib.parse import urljoin
from engine4.constants import ENDPOINTS
from engine4.exceptions import HttpResponseException
from engine4.utils import create_authorization_header



class AuthenticateResult:
    def __init__(self, access_token, expires_in, token_type, refresh_token, scope):
        self.access_token = access_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.refresh_token = refresh_token
        self.scope = scope

class FetchFilterOptions:
    def __init__(self, generic_name, compare_operator, value):
        self.generic_name = generic_name
        self.compare_operator = compare_operator
        self.value = value


class ENGINE4:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def authenticate(
            self,
            username: str,
            password: str,
            client_id: str,
    ) -> AuthenticateResult:
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
        }
        data = {
            'grant_type': 'password',
            'username': username,
            'password': password,
            'client_id': client_id,
        }
        method = 'POST'
        url = urljoin(self.base_url, ENDPOINTS.TOKEN)
        response = requests.request(method, url, data=data, headers=headers)
        if not response.ok:
            raise HttpResponseException(response.status_code, response.reason, response.json())
        response_json = response.json()
        return AuthenticateResult(response_json['access_token'], response_json['expires_in'], response_json['token_type'], response_json['refresh_token'], response_json['scope'])


    def fetch(
            self,
            accessToken: str,
            entity_id: str,
            skip: int,
            take: int,
            with_long_values: bool,
            is_active: bool,
            filter: FetchFilterOptions = None
    ) -> dict:
        headers = {
            'Accept': 'application/json',
            'Authorization': create_authorization_header(accessToken),
            'Content-Type': 'application/json',
        }
        data = {
            'EntityId': entity_id,
            'Skip': skip,
            'Take': take,
            'WithLongValues': with_long_values,
            'IsActive': is_active
        }
        if filter != None:
            data['Filter'] = {
                'GenericName': filter.generic_name,
                'CompareOperator': filter.compare_operator,
                'Value': filter.value,
            }
        response = requests.post(
            urljoin(self.base_url, ENDPOINTS.FETCH), json=data, headers=headers)
        response_json = response.json()
        return {
            'items': response_json
        }
