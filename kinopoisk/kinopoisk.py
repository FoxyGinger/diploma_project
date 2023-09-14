import sys
from enum import Enum

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
        self.__main_url = config.get("server")
        self.__token = config.get("token")
        self.__endpoints = config.get("endpoints")
        self.__schema_checker = SchemaChecker(config.get("response_schemas_folder"))

    def __get(self, path: str, params: dict = None, token: str = None) -> requests.Response:
        token = self.__token if token is None else token
        full_url = f"{self.__main_url}/{path}"
        response = requests.get(url=full_url, params=params, headers={
            "Accept": "application/json",
            "Accept-Encoding": "identity",
            "X-API-KEY": token,
        }, timeout=15)

        return response

    def movie_random(self, token: str = None) -> ResponseKp:
        endpoint = 'movie_random'
        resp = self.__get(path=self.__get_path_by_endpoint(endpoint), token=token)

        return ResponseKp(response=resp, endpoint=endpoint)

    def health(self, token: str = None) -> ResponseKp:
        endpoint = 'health'
        resp = self.__get(path=self.__get_path_by_endpoint(endpoint), token=token)

        return ResponseKp(response=resp, endpoint=endpoint)

    def movie_possible_values_by_field(self, field: str, token: str = None) -> ResponseKp:
        endpoint = 'movie_possible_values_by_field'
        resp = self.__get(path=self.__get_path_by_endpoint(endpoint), params={"field": field}, token=token)

        return ResponseKp(response=resp, endpoint=endpoint)

    def movie_awards(self, token: str = None, params: dict = None) -> ResponseKp:
        endpoint = 'movie_awards'
        resp = self.__get(path=self.__get_path_by_endpoint(endpoint), token=token, params=params)

        return ResponseKp(response=resp, endpoint=endpoint)

    def movie_search(self, text: str, token: str = None, params: dict = None) -> ResponseKp:
        endpoint = 'movie_search'
        parameters = {"query": text}
        if params is not None:
            parameters.update(params)

        resp = self.__get(path=self.__get_path_by_endpoint(endpoint), params=parameters, token=token)

        return ResponseKp(response=resp, endpoint=endpoint)

    def check_response_code(self, response: ResponseKp, expected_code: int):
        with allure.step(f'Проверка кода возврата "{expected_code}" на запрос "{response.response.request.method}" "{response.response.request.path_url}"'):
            if response.response.status_code != expected_code:
                print(f'Error text: "{response.json()}"', file=sys.stderr)
                pytest.fail(
                    f'Response "{response.url}" status code({response.status_code}) != expected_code({expected_code})')

    def check_response_body_keys(self, response: [ResponseKp | dict], expected_keys: set = None):
        with allure.step(f'Проверка тела ответа на запрос "{response.response.request.method}" "{response.response.request.path_url}"'):
            self.check_response_code(response, expected_code=200)
            if expected_keys is None:
                expected_keys = response.endpoint

            if not self.__schema_checker.check_field_keys(actual_data=response.json(), expected_keys=expected_keys):
                pytest.fail(f'Invalid response body "{response.url}"')

    def check_json_keys(self, json: dict, expected_keys: set):
        with allure.step(f'Проверка наличие ключей "{expected_keys}" в json'):
            if not self.__schema_checker.check_field_keys(actual_data=json, expected_keys=expected_keys):
                pytest.fail(f'Invalid json keys: "{json.keys()}"')

    def get_expected_body_response(self, response: ResponseKp) -> dict:
        return self.__schema_checker.get_schema_data(response.endpoint)

    def __get_path_by_endpoint(self, endpoint: str) -> str:
        params = self.__endpoints.get(endpoint)
        ver = params.get('ver')
        path = params.get('path')

        return f'{ver}/{path}'

