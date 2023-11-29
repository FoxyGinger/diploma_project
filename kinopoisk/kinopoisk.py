import pytest
import requests

from qaseio.pytest import qase


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

    def check_response_code(self, expected_code: int):
        with qase.step(f'Проверить статус кода ответа', expected=f'{expected_code}'):
            if self.status_code != expected_code:
                print(f'Error text: "{self.json()}"')
                pytest.fail(
                    f'Response "{self.url}" status code({self.status_code}) != expected_code({expected_code})')

    def check_field_keys(self, expected_fields: set, nested_fields: list = None):
        with qase.step(f'Проверить поля ответа: {expected_fields}', expected='Поля содержаться'):
            actual_fields = self.json().keys() if nested_fields is None else self.__get_nested_object(
                nested_fields).keys()
            success = expected_fields <= actual_fields
            if not success:
                pytest.fail(f'Absent fields: "{expected_fields ^ actual_fields}"')

    def check_field_values(self, expected_field_values: dict, nested_fields: list = None):
        with qase.step(f'Проверить значения полей ответа: {expected_field_values}', expected='Значения полей ожидаемые'):
            actual_fields_values = self.json() if nested_fields is None else self.__get_nested_object(nested_fields)
            for field_key, field_value in expected_field_values.items():
                if field_key not in actual_fields_values.keys():
                    pytest.fail(f'Absent field: "{field_key}"')

                if actual_fields_values.get(field_key) != field_value:
                    pytest.fail(
                        f'filed {field_key}: {actual_fields_values.get(field_key)} (actual) != {field_value} (expected)')

    def check_object_count(self, field_name: str, count: int, nested_fields: list = None):
        with qase.step(f'Проверить количество элементов в ответе в поле "{field_name}', expected=f'{count}'):
            actual_fields_values = self.json() if nested_fields is None else self.__get_nested_object(nested_fields)
            if field_name not in actual_fields_values.keys():
                pytest.fail(f'Absent field: "{field_name}"')

            if len(actual_fields_values.get(field_name)) != count:
                pytest.fail(
                    f'element count in "{field_name}": {len(actual_fields_values.get(field_name))} (actual) != {count} (expected)')

    def __get_nested_object(self, nested_fields: list):
        nested_object = self.json()
        for field in nested_fields:
            if field not in nested_object.keys():
                pytest.fail(f'filed {field} does not exist')

            nested_object = nested_object.get(field)

        return nested_object


class Kinopoisk:
    __main_url: str
    __endpoints: dict
    __token: str

    def __init__(self, config: dict):
        self.__config = config
        self.__main_url = config.get("server")
        self.__token = config.get("token")
        self.__endpoints = config.get("endpoints")

    def __get(self, path: str, params: dict = None, token: str = None) -> requests.Response:
        token = self.__token if token is None else token
        full_url = f"{self.__main_url}/{path}"
        with qase.step(f'Отправить GET запрос: "{full_url}"', expected="Запрос отправлен"):
            response = requests.get(url=full_url, params=params, headers={
                "Accept": "application/json",
                "Accept-Encoding": "identity",
                "X-API-KEY": token,
            }, timeout=45)

            return response

    def movie(self, params: dict = None, token: str = None) -> ResponseKp:
        endpoint = 'movie'
        resp = self.__get(path=self.__get_path_by_endpoint(endpoint), params=params, token=token)

        return ResponseKp(response=resp, endpoint=endpoint)

    def movie_random(self, token: str = None) -> ResponseKp:
        endpoint = 'movie_random'
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

    def movie_by_id(self, movie_id: [int | str], token: str = None) -> ResponseKp:
        endpoint = 'movie_id'

        resp = self.__get(path=self.__get_path_by_endpoint(endpoint).format(id=movie_id), token=token)

        return ResponseKp(response=resp, endpoint=endpoint)

    def __get_path_by_endpoint(self, endpoint: str) -> str:
        params = self.__endpoints.get(endpoint)
        ver = params.get('ver')
        path = params.get('path')

        return f'{ver}/{path}'
