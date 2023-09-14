from kinopoisk.kinopoisk import *


@allure.id("2000")
@allure.title('Movie.Fields. Проверка запроса значений для "genres.name"')
@allure.suite("Regression")
@allure.sub_suite("Movie")
@allure.feature("Movie")
@pytest.mark.Smoke
@pytest.mark.Regression
def test_possible_values_genres_name(kinopoisk: Kinopoisk):
    with allure.step("1. Отправка запроса"):
        resp = kinopoisk.movie_possible_values_by_field("genres.name")
    with allure.step("2. Проверка кода 200"):
        kinopoisk.check_response_code(resp, 200)
    with allure.step("3. Проверка тела ответа"):
        response_body = resp.json()
        if not isinstance(response_body, list):
            pytest.fail(f'Для поля "genres.name" тело ответа должно быть "array"')
        if len(response_body) == 0:
            pytest.fail(f'Для поля "genres.name" тело ответа не должно быть пустым массивом')
        kinopoisk.check_json_keys(response_body[0], {"name", "slug"})


@allure.id("2001")
@allure.title('Movie.Fields. Проверка запроса значений для "countries.name"')
@allure.suite("Regression")
@allure.sub_suite("Movie")
@allure.feature("Movie")
@pytest.mark.Smoke
@pytest.mark.Regression
def test_possible_values_countries_name(kinopoisk: Kinopoisk):
    with allure.step("1. Отправка запроса"):
        resp = kinopoisk.movie_possible_values_by_field("countries.name")
    with allure.step("2. Проверка кода 200"):
        kinopoisk.check_response_code(resp, 200)
    with allure.step("3. Проверка тела ответа"):
        response_body = resp.json()
        if not isinstance(response_body, list):
            pytest.fail(f'Для поля "countries.name" тело ответа должно быть "array"')
        if len(response_body) == 0:
            pytest.fail(f'Для поля "countries.name" тело ответа не должно быть пустым массивом')
        kinopoisk.check_json_keys(response_body[0], {"name", "slug"})


@allure.id("2002")
@allure.title('Movie.Fields. Проверка запроса значений для "type"')
@allure.suite("Regression")
@allure.sub_suite("Movie")
@allure.feature("Movie")
@pytest.mark.Smoke
@pytest.mark.Regression
def test_possible_values_type(kinopoisk: Kinopoisk):
    with allure.step("1. Отправка запроса"):
        resp = kinopoisk.movie_possible_values_by_field("type")
    with allure.step("2. Проверка кода 200"):
        kinopoisk.check_response_code(resp, 200)
    with allure.step("3. Проверка тела ответа"):
        response_body = resp.json()
        if not isinstance(response_body, list):
            pytest.fail(f'Для поля "type" тело ответа должно быть "array"')
        if len(response_body) == 0:
            pytest.fail(f'Для поля "type" тело ответа не должно быть пустым массивом')
        kinopoisk.check_json_keys(response_body[0], {"name", "slug"})


@allure.id("2003")
@allure.title('Movie.Fields. Проверка запроса значений для "typeNumber"')
@allure.suite("Regression")
@allure.sub_suite("Movie")
@allure.feature("Movie")
@pytest.mark.Smoke
@pytest.mark.Regression
def test_possible_values_type_number(kinopoisk: Kinopoisk):
    with allure.step("1. Отправка запроса"):
        resp = kinopoisk.movie_possible_values_by_field("typeNumber")
    with allure.step("2. Проверка кода 200"):
        kinopoisk.check_response_code(resp, 200)
    with allure.step("3. Проверка тела ответа"):
        response_body = resp.json()
        if not isinstance(response_body, list):
            pytest.fail(f'Для поля "typeNumber" тело ответа должно быть "array"')
        if len(response_body) == 0:
            pytest.fail(f'Для поля "typeNumber" тело ответа не должно быть пустым массивом')
        kinopoisk.check_json_keys(response_body[0], {"name", "slug"})


@allure.id("2004")
@allure.title('Movie.Fields. Проверка запроса значений для "status"')
@allure.suite("Regression")
@allure.sub_suite("Movie")
@allure.feature("Movie")
@pytest.mark.Smoke
@pytest.mark.Regression
def test_possible_values_status(kinopoisk: Kinopoisk):
    with allure.step("1. Отправка запроса"):
        resp = kinopoisk.movie_possible_values_by_field("status")
    with allure.step("2. Проверка кода 200"):
        kinopoisk.check_response_code(resp, 200)
    with allure.step("3. Проверка тела ответа"):
        response_body = resp.json()
        if not isinstance(response_body, list):
            pytest.fail(f'Для поля "status" тело ответа должно быть "array"')
        if len(response_body) == 0:
            pytest.fail(f'Для поля "status" тело ответа не должно быть пустым массивом')
        kinopoisk.check_json_keys(response_body[0], {"name", "slug"})
