from kinopoisk.kinopoisk import *


@allure.id("1")
@allure.title("Health. Проверка работоспособности сервера")
@allure.suite("Smoke")
@allure.sub_suite("Health")
@allure.feature("Health")
@pytest.mark.Smoke
@pytest.mark.Regression
def test_health(kinopoisk: Kinopoisk):
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
        if error_count != 0:
            pytest.fail(f'Server has "{error_count}" errors')


@allure.id("2")
@allure.title("Health. Запрос с невалидным токеном")
@allure.suite("Regression")
@allure.sub_suite("Health")
@allure.feature("Health")
@pytest.mark.Regression
def test_invalid_token(kinopoisk: Kinopoisk):
    with allure.step("1. Отправка запроса на рандомный фильм"):
        resp = kinopoisk.health(token="1321334213")
    with allure.step("2. Проверка кода 401"):
        kinopoisk.check_response_code(resp, 401)
    with allure.step("3. Проверка тела ответа"):
        body = resp.json()
        status_code = body.get("statusCode")
        if status_code != 401:
            pytest.fail(f'statusCode({status_code}) != 401')
        error = body.get("error")
        if error != "Unauthorized":
            pytest.fail(f'error({error}) != Unauthorized')
        message = body.get("message")
        if message != 'Переданный токен некорректен!':
            pytest.fail(f'message({message}) != "Переданный токен некорректен!"')


@allure.id("3")
@allure.title("Health. Запрос с пустым токеном")
@allure.suite("Regression")
@allure.sub_suite("Health")
@allure.feature("Health")
@pytest.mark.Regression
def test_empty_token(kinopoisk: Kinopoisk):
    with allure.step("1. Отправка запроса на рандомный фильм"):
        resp = kinopoisk.movie_random(token="")
    with allure.step("2. Проверка кода 401"):
        kinopoisk.check_response_code(resp, 401)
    with allure.step("3. Проверка тела ответа"):
        body = resp.json()
        status_code = body.get("statusCode")
        if status_code != 401:
            pytest.fail(f'statusCode({status_code}) != 401')
        error = body.get("error")
        if error != "Unauthorized":
            pytest.fail(f'error({error}) != Unauthorized')
        message = body.get("message")
        if message != 'В запросе не указан токен!':
            pytest.fail(f'message({message}) != "В запросе не указан токен!"')
