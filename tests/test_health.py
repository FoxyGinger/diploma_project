from kinopoisk.kinopoisk import *


@allure.id("999")
@allure.title("Health. Проверка работоспособности сервера")
@allure.suite("Smoke")
@allure.sub_suite("Health")
@allure.feature("Health")
@pytest.mark.Smoke
@pytest.mark.Regression
def test_movie_random(kinopoisk: Kinopoisk):
    with allure.step("1. Отправка запроса"):
        resp = kinopoisk.health()
    with allure.step("2. Проверка кода 200"):
        kinopoisk.check_response_code(resp, 200)
    with allure.step("3. Проверка тела ответа"):
        kinopoisk.check_response_body(resp)
    with allure.step("4. Проверка статуса"):
        status = resp.json().get("status")
        if status != "ok":
            pytest.fail(f'Server status is "{status}"')
    with allure.step("4. Проверка ошибок на сервере"):
        error_count = len(resp.json().get("error"))
        if error_count != 0 :
            pytest.fail(f'Server has "{error_count}" errors')
