import random

from kinopoisk.kinopoisk import *


@allure.id("5000")
@allure.title("Movie.Id. Проверка запроса")
@allure.suite("Smoke")
@allure.sub_suite("Movie")
@allure.feature("Movie")
@pytest.mark.Smoke
@pytest.mark.Regression
def test_movie_search(kinopoisk: Kinopoisk):
    # Генерируем рандомный id
    movie_id = random.randrange(1, 973064)
    with allure.step("1. Отправка запроса"):
        resp = kinopoisk.movie_by_id(movie_id=movie_id)
    with allure.step("2. Проверка кода 200"):
        kinopoisk.check_response_code(resp, 200)
    with allure.step("3. Проверка тела ответа"):
        kinopoisk.check_response_body_keys(resp)
    with allure.step("3. Проверяем, что id фильма совпадает с запрошенным"):
        movies = resp.json().get('docs')
        for movie in movies:
            id = movie.get('id')
            if id != movie_id:
                pytest.fail(f'Id фильма в запросе "{movie_id}" не совпадает с id в ответе "{id}"')

