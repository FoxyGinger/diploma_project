from kinopoisk.kinopoisk import *


@allure.id("1000")
@allure.title("Movie.Random. Проверка запроса")
@allure.suite("Smoke")
@allure.sub_suite("Movie")
@allure.feature("Movie")
@pytest.mark.Smoke
@pytest.mark.Regression
def test_movie_random(kinopoisk: Kinopoisk):
    with allure.step("1. Отправка запроса на рандомный фильм"):
        resp = kinopoisk.movie_random()
    with allure.step("2. Проверка кода 200"):
        kinopoisk.check_response_code(resp, 200)
    with allure.step("3. Проверка тела ответа"):
        kinopoisk.check_response_body(resp)


@allure.id("1001")
@allure.title("Movie.Random. Проверка рандомности")
@allure.suite("Regression")
@allure.sub_suite("Movie")
@allure.feature("Movie")
@pytest.mark.Regression
@pytest.mark.xfail(condition=lambda: True, reason='Тест может упасть так как запрос может вернуть 2 одинаковых фильма')
def test_movie_random_2_movies(kinopoisk: Kinopoisk):
    with allure.step("1. Отправка запроса на первый рандомный фильм"):
        movie1_resp = kinopoisk.movie_random()
    with allure.step("2. Отправка запроса на второй рандомный фильм"):
        movie2_resp = kinopoisk.movie_random()
    with allure.step("2. Проверка, что запросы выполнены успешно"):
        kinopoisk.check_response_code(movie1_resp, 200)
        kinopoisk.check_response_code(movie2_resp, 200)
    with allure.step("4. Проверяем, что фильмы разные"):
        movie1_id = movie1_resp.json().get("id")
        movie2_id = movie2_resp.json().get("id")
        if movie1_id == movie2_id:
            pytest.fail(f"Фильмы не уникальны: movie1_id({movie1_id}) == movie2_id({movie2_id})")
