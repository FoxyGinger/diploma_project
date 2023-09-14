from kinopoisk.kinopoisk import *


@allure.id("4000")
@allure.title("Movie.Search. Проверка запроса")
@allure.suite("Smoke")
@allure.sub_suite("Movie")
@allure.feature("Movie")
@pytest.mark.Smoke
@pytest.mark.Regression
def test_movie_search(kinopoisk: Kinopoisk):
    with allure.step("1. Отправка запроса"):
        resp = kinopoisk.movie_search('Тор')
    with allure.step("2. Проверка кода 200"):
        kinopoisk.check_response_code(resp, 200)
    with allure.step("3. Проверка тела ответа"):
        kinopoisk.check_response_body_keys(resp)
