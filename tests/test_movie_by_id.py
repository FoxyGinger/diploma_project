from kinopoisk.kinopoisk import *

from qaseio.pytest import qase


movie_id = 22222
invalid_movie_id = "12845%$"
invalid_token = "invalid_token"


@qase.id(1)
@qase.suite("Поиск фильма по id (фильмы, сериалы)")
@qase.title("Получение фильма по существующему корректно заданному id")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_id(kinopoisk: Kinopoisk):
    resp = kinopoisk.movie_id(movie_id=movie_id)
    resp.check_response_code(200)
    resp.check_field_values(expected_field_values={"id": movie_id})


@qase.id(2)
@qase.suite("Поиск фильма по id (фильмы, сериалы)")
@qase.title("Получение фильма по некорректно заданному id")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "negative"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_id_invalid_id(kinopoisk: Kinopoisk):
    resp = kinopoisk.movie_id(movie_id=invalid_movie_id)
    resp.check_response_code(400)


@qase.id(4)
@qase.suite("Поиск фильма по id (фильмы, сериалы)")
@qase.title("Получение фильма без авторизации")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "negative"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_id_invalid_token(kinopoisk: Kinopoisk):
    resp = kinopoisk.movie_id(movie_id=movie_id, token=invalid_token)
    resp.check_response_code(401)

