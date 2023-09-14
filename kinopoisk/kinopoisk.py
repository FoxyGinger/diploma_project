import pytest
import requests
import allure

from kinopoisk.schema_checker import SchemaChecker


class ResponseKp:
    response: requests.Response
    endpoint: str

    def __init__(self, response: requests.Response, endpoint: str):
        self.response = response
        self.endpoint = endpoint

    @property
    def status_code(self) -> int:
        return self.response.status_code

    @property
    def url(self) -> str:
        return self.response.url

    def json(self) -> dict:
        return self.response.json()


class Kinopoisk:
    __main_url: str
    __endpoints: dict
    __token: str
    __schema_checker: SchemaChecker

    def __init__(self, config: dict):
        self.__config = config
        server = config.get("server")
        api_version = config.get("version")
        self.__main_url = f"{server}/{api_version}"
        self.__token = config.get("token")
        self.__endpoints = config.get("endpoints")
        self.__schema_checker = SchemaChecker(config.get("response_schemas_folder"), api_version)

    def __get(self, endpoint: str, params: dict = None, token: str = None) -> ResponseKp:
        token = self.__token if token is None else token
        full_url = f"{self.__main_url}/{endpoint}"
        response = requests.get(url=full_url, params=params, headers={
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "X-API-KEY": token,
        }, timeout=15)

        return ResponseKp(response, endpoint)

    def movie_random(self, token: str = None) -> ResponseKp:
        return self.__get(endpoint=self.__endpoints.get('random'), token=token)

    def health(self, token: str = None):
        return self.__get(endpoint=self.__endpoints.get('health'), token=token)

    def check_response_code(self, response: ResponseKp, expected_code: int):
        with allure.step(f'Проверка кода возврата "{expected_code}" на запрос "{response.response.request.method}" "{response.response.request.path_url}"'):
            if response.response.status_code != expected_code:
                pytest.fail(
                    f'Response "{response.url}" status code({response.status_code}) != expected_code({expected_code})')

    def check_response_body(self, response: ResponseKp, expected_body: dict = None):
        with allure.step(f'Проверка тела ответа на запрос "{response.response.request.method}" "{response.response.request.path_url}"'):
            self.check_response_code(response, expected_code=200)
            if expected_body is None:
                expected_body = response.endpoint

            if not self.__schema_checker.check_field_keys(actual_data=response.json(), expected_data=expected_body):
                pytest.fail(f'Invalid response body "{response.url}"')
