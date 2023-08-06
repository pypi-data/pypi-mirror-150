import requests
from elasticsearch_dsl import Search
from elasticsearch_dsl.response import Response
from minetext.config import Config
from minetext.domain.es_request import EsRequest


class Mine:
    _host: str
    _es_request: EsRequest
    _internal_token: str
    _device_code: str
    _user_code: str
    _verification_uri: str
    _verification_uri_complete: str
    _access_token: str
    _refresh_token: str

    def __init__(self, es_request: EsRequest, host: str = Config.host):
        """
        Initialize the MINE object.

        :param host: the endpoint of the REST API
        :param es_request: the object containing request information to Elasticsearch
        """
        self._host = host
        self._es_request = es_request
        self._device_code = ''
        self._user_code = ''
        self._verification_uri = ''
        self._verification_uri_complete = ''
        self._access_token = ''
        self._refresh_token = ''

    def search(self) -> Response:
        """
        Call the search endpoint with parameters provided via the ``_es_request`` property.

        :return: the result wrapped in the ``Response`` object
        """
        url = f'{self._host}/document/search'

        payload = {
            'q': self._es_request.search_term,
            'f[]': self._es_request.filters,
            'a': self._es_request.aggregation,
            'p': self._es_request.page,
            's': self._es_request.size,
            'wa': self._es_request.analytics
        }

        if not self._access_token:
            headers = {
                'Authorization': f'Bearer {self._access_token}'
            }
            result = requests.get(url, params=payload, headers=headers)
        else:
            result = requests.get(url, params=payload)

        # Parse the result using Elasticsearch Response
        response = Response(Search(), result.json())

        return response

    def _create_device_token(self) -> None:
        """Sets device token from mine-graph-api.

        Sets the uris, device_code and user_code from response.

        Raises
        -------
        HTTPError
            When device token could not be created.
        """
        device_token_response = requests.get(f'{self.host}/auth/device_token')
        device_token_response.raise_for_status()
        token_json = device_token_response.json()
        self._device_code = token_json['device_code']
        self._user_code = token_json['user_code']
        self._verification_uri = token_json['verification_uri']
        self._verification_uri_complete = token_json['verification_uri_complete']

    def _create_access_token(self) -> None:
        """Sets access token from authentication.

        Posts the device_code to MINE-API. If the user logged in properly
        the device code should now authorize them. Sets the access_token of Auth object.

        Raises
        -------
        HTTPError
            When access token could not be created. This happens mostly when the user did not log in properly
            but stated they did so.
        """
        token_response = requests.post(f'{self.host}/auth/token', json={'device_code': self._device_code})
        token_response.raise_for_status()
        token_json = token_response.json()
        self._access_token = token_json['access_token']
        self._refresh_token = token_json['refresh_token']
        print('Login successful! You are now authorized.')

    def login(self) -> None:
        """Calls the functions to authorize user.

        Waits for the user to log in into the verification uri and afterwards creates an access token if the user
        stated they granted access.
        """
        self._create_device_token()
        print(f'Please sign in at this website and grant access: {self._verification_uri_complete}')
        input_str = input('Did you grant the access? [y/N]')
        if input_str != 'y':
            return
        self._create_access_token()

    def get_identifiers(self):
        """
        Call the get_identifiers endpoint

        :return: the result return list of identifiers
        """
        result = self.search()

        response = []
        for hit in result.hits:
            identifier = hit.meta.id
            response.append(identifier)

        return response

    @property
    def host(self):
        return self._host

    @host.setter
    def host(self, value):
        self._host = value

    @property
    def es_request(self):
        return self._es_request

    @es_request.setter
    def es_request(self, value):
        self._es_request = value
