"""
Тесты для метода movie/possible-values-by-field
"""
from kinopoisk.kinopoisk import *


@qase.id(43)
@qase.title("Получение списка стран")
@qase.suite("Получение списков стран, жанров (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated"))
def test_movie_values_field_country_name(kinopoisk: Kinopoisk):
    """
    Получение списка стран
    :param kinopoisk:
    :return:
    """
    field = "countries.name"
    resp = kinopoisk.movie_possible_values_by_field(field=field)
    resp.check_response_code(200)
    with qase.step('Проверить что в ответе не пустой список полей "{field}"', expected='список не пустой'):
        values = resp.json()
        assert len(values) > 0, "Список пустой"


@qase.id(44)
@qase.title("Получение списка жанров")
@qase.suite("Получение списков стран, жанров (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated"))
def test_movie_values_field_genres_name(kinopoisk: Kinopoisk):
    """
    Получение списка жанров
    :param kinopoisk:
    :return:
    """
    field = "genres.name"
    resp = kinopoisk.movie_possible_values_by_field(field=field)
    resp.check_response_code(200)
    with qase.step(f'Проверить что в ответе не пустой список полей "{field}"', expected='список не пустой'):
        values = resp.json()
        assert len(values) > 0, "Список пустой"


@qase.id(45)
@qase.title("Получение списка типов")
@qase.suite("Получение списков стран, жанров (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated"))
def test_movie_values_field_type_name(kinopoisk: Kinopoisk):
    """
    Получение списка типов
    :param kinopoisk:
    :return:
    """
    field = "type"
    resp = kinopoisk.movie_possible_values_by_field(field=field)
    resp.check_response_code(200)
    with qase.step(f'Проверить что в ответе не пустой список полей "{field}"', expected='список не пустой'):
        values = resp.json()
        assert len(values) > 0, "Список пустой"


@qase.id(46)
@qase.title("Получение списка статусов")
@qase.suite("Получение списков стран, жанров (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated"))
def test_movie_values_field_status_name(kinopoisk: Kinopoisk):
    """
    Получение списка статусов
    :param kinopoisk:
    :return:
    """
    field = "status"
    resp = kinopoisk.movie_possible_values_by_field(field=field)
    resp.check_response_code(200)
    with qase.step(f'Проверить что в ответе не пустой список полей "{field}"', expected='список не пустой'):
        values = resp.json()
        assert len(values) > 0, "Список пустой"
