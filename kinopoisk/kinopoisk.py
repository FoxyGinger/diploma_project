import pytest
import requests
import httpx

from kinopoisk.schema_checker import SchemaChecker


class Kinopoisk:
    __main_url: str
    __urls: dict
    __token: str
    __schema_checker: SchemaChecker

    def __init__(self, config: dict):
        self.__config = config
        server = config.get("server")
        api_version = config.get("version")
        self.__main_url = f"{server}/{api_version}"
        self.__token = config.get("token")
        self.__urls = config.get("urls")
        self.__schema_checker = SchemaChecker(config.get("response_schemas_folder"), api_version)

    def __get(self, url: str, params: dict = None, token: str = None) -> requests.Response:
        if token is None:
            token = self.__token

        full_url = f"{self.__main_url}/{self.__urls.get(url)}"
        return requests.get(url=full_url, params=params, headers={
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "X-API-KEY": token,
        }, timeout=15)

    def movie_random(self, token: str = None) -> requests.Response:
        return self.__get(url="random", token=token)

    def check_response_code(self, response: requests.Response, expected_code: int):
        if response.status_code != expected_code:
            pytest.fail(
                f'Response "{response.url}" status code({response.status_code}) != expected_code({expected_code})')

    def check_response_body(self, response: requests.Response, schema_name: str, nested_keys: list = None):
        self.check_response_code(response, expected_code=200)
        if not self.__schema_checker.check_field_keys(schema_name=schema_name, data=response.json(),
                                                      nested_keys=nested_keys):
            pytest.fail(f'Invalid response body "{response.url}"')
