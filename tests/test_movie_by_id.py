import random

from kinopoisk.kinopoisk import *


movie_id = 22222


@allure.id("5000")
@allure.title("Movie.Id. Проверка запроса")
@allure.suite("Smoke")
@allure.sub_suite("Movie")
@allure.feature("Movie")
@pytest.mark.Smoke
@pytest.mark.Regression
def test_movie_by_id(kinopoisk: Kinopoisk):
    with allure.step("1. Отправка запроса"):
        resp = kinopoisk.movie_by_id(movie_id=movie_id)
    with allure.step("2. Проверка кода 200"):
        kinopoisk.check_response_code(resp, 200)
    with allure.step("3. Проверяем, что id фильма совпадает с запрошенным"):
        current_id = resp.json().get('id')
        if current_id != movie_id:
            pytest.fail(f'Id фильма в запросе "{movie_id}" не совпадает с id в ответе "{current_id}"')

