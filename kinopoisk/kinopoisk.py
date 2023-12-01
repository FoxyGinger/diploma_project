import inspect

import requests
from qaseio.pytest import qase


class ResponseKp:
    response: requests.Response

    def __init__(self, response: requests.Response):
        self.response = response

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
            assert self.status_code == expected_code, \
                f'Код ответа на "{self.url}" {self.status_code}(фактический) != {expected_code}(ожидаемый)'

    def get_movies(self) -> list:
        return self.__get_objects_by_type("movie")

    def get_awards(self) -> list:
        return self.__get_objects_by_type("awards")

    def __get_objects_by_type(self, object_type: str) -> list:
        assert object_type in self.response.url, f'запрос не относился к "{object_type}": {self.response.url}'
        try:
            assert len(self.json().keys()) > 0, f"Некорректное тело ответа: {self.json()}"
            if "docs" in self.json().keys():
                return self.json().get("docs")

            return [self.json()]
        except AttributeError:
            assert False, f"Некорректное тело ответа: {self.response.text}"


class Kinopoisk:
    __main_url: str
    __endpoints: dict
    __token: str
    __request_timeout: int

    def __init__(self, config: dict):
        """
        Обертка клиента api.kinopoisk.dev
        :param config: словарь с параметрами
        """
        self.__config = config
        self.__main_url = config.get("server")
        self.__token = config.get("token")
        self.__endpoints = config.get("endpoints")
        self.__request_timeout = config.get("request_timeout")

    def __get(self, path: str, path_params: dict = None, query_params: dict = None, token: str = None,
              timeout: int = None) -> requests.Response:
        """
        Основной метод выполняющий GET запрос.
        :param path:
        :param query_params:
        :param token:
        :param timeout:
        :return:
        """
        path = self.__set_path_params(path, path_params=path_params)
        self.__query_params_by_test_case_step(query_params=query_params)
        if token is not None:
            with qase.step('Использовать невалидный токен', expected=f'в заголовке "X-API-KEY": {token}'):
                pass
        else:
            token = self.__token

        if timeout is not None:
            with qase.step('Выставить таймаут для запроса', expected=f'ожидание ответа не более {timeout} секунд'):
                pass
        else:
            timeout = self.__request_timeout

        full_url = f"{self.__main_url}/{path}"
        with qase.step(f'Отправить GET запрос: "{full_url}"', expected="Запрос отправлен"):
            try:
                response = requests.get(url=full_url, params=query_params, headers={
                    "Accept": "application/json",
                    "Accept-Encoding": "identity",
                    "X-API-KEY": token,
                }, timeout=timeout)

                return response
            except requests.Timeout:
                assert False, f"Таймаут запроса: {timeout}"

    def movie(self, query_params: dict = None, token: str = None, timeout: int = None) -> ResponseKp:
        """
        Этот метод вернет список фильмов удовлетворяющих вашему запросу.
        В ответе придут поля указанные в параметре selectFields.
        Если его не указать, то вернутся только дефолтные поля.
        :param query_params:
        :param token:
        :param timeout:
        :return:
        """
        resp = self.__get(path=self.__get_path_by_caller_function(), query_params=query_params, token=token,
                          timeout=timeout)

        return ResponseKp(response=resp)

    def movie_id(self, movie_id: [int | str], token: str = None, timeout: int = None) -> ResponseKp:
        """
        Возвращает всю доступную информацию о сущности.
        :param movie_id:
        :param token:
        :param timeout:
        :return:
        """
        resp = self.__get(path=self.__get_path_by_caller_function(), path_params={"id": movie_id}, token=token,
                          timeout=timeout)

        return ResponseKp(response=resp)

    def movie_random(self, query_params: dict = None, token: str = None, timeout: int = None) -> ResponseKp:
        """
        Этот метод вернет рандомный тайтл из базы.
        Вы можете составить фильтр, чтобы получить рандомный тайтл по вашим критериям.
        :param query_params:
        :param token:
        :param timeout:
        :return:
        """
        resp = self.__get(path=self.__get_path_by_caller_function(), query_params=query_params, token=token, timeout=timeout)

        return ResponseKp(response=resp)

    def movie_search(self, text: str, token: str = None, query_params: dict = None, timeout: int = None) -> ResponseKp:
        """
        Метод вернет список фильмов которые подходят под ваш запрос.
        :param text:
        :param token:
        :param query_params:
        :param timeout:
        :return:
        """
        parameters = {"query": text}
        if query_params is not None:
            parameters.update(query_params)

        resp = self.__get(path=self.__get_path_by_caller_function(), query_params=parameters, token=token,
                          timeout=timeout)

        return ResponseKp(response=resp)

    def movie_possible_values_by_field(self, field: str, token: str = None, timeout: int = None) -> ResponseKp:
        """
        Этот метод принимает только определенные поля, и возвращает по ним все доступные значения.
        :param field:
        :param token:
        :param timeout:
        :return:
        """
        resp = self.__get(path=self.__get_path_by_caller_function(), query_params={"field": field}, token=token,
                          timeout=timeout)

        return ResponseKp(response=resp)

    def movie_awards(self, token: str = None, query_params: dict = None, timeout: int = None) -> ResponseKp:
        """
        Возвращает награды тайтлов.
        :param token:
        :param query_params:
        :param timeout:
        :return:
        """
        resp = self.__get(path=self.__get_path_by_caller_function(), token=token, query_params=query_params,
                          timeout=timeout)

        return ResponseKp(response=resp)

    def __get_path_by_caller_function(self) -> str:
        """
        Метод позволяет получить полный url для запроса на основании имени метода, в котором он был вызван.
        Имена методов должны совпадать с endpoints в конфиге.
        :return:
        """
        function_name = inspect.stack()[1][3]
        params = self.__endpoints.get(function_name)
        ver = params.get('ver')
        path = params.get('path')

        return f'{ver}/{path}'

    def __set_path_params(self, path: str, path_params: dict) -> str:
        """
        Вспомогательный метод. Заполняет path-параметры и раскладывает каждый парметр как шаг для тест-кейса.
        :param path:
        :param path_params:
        :return:
        """
        if path_params is None:
            return path

        for param, value in path_params.items():
            with qase.step(f'Установить path-параметр "{param}" со значением "{value}"'):
                pass

        return path.format(**path_params)

    def __query_params_by_test_case_step(self, query_params: dict):
        """
        Вспомогательный метод. Раскладывает каждый query-парметр как шаг для тест-кейса.
        :param query_params:
        :return:
        """
        if query_params is None:
            return

        for param, value in query_params.items():
            with qase.step(f'Установить query-параметр "{param}" со значением "{value}"'):
                pass
