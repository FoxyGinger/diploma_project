from kinopoisk.kinopoisk import *

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


@qase.id(324)
@qase.title("Получение фильмов не на первой странице")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_id_another_page(kinopoisk: Kinopoisk):
    page1 = 2
    resp1 = kinopoisk.movie(query_params={
        "page": page1
    })
    resp1.check_response_code(200)
    movies1 = resp1.get_movies()
    page2 = 3
    resp2 = kinopoisk.movie(query_params={
        "page": page2
    })
    resp2.check_response_code(200)
    movies2 = resp2.get_movies()
    for movie in movies2:
        assert movie not in movies1, f"Есть пересечения фильмов с {page1} страницы с {page2} страницой"


@qase.id(325)
@qase.title("Получение фильмов c измененным количеством элементов на странице")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_id_page_limit(kinopoisk: Kinopoisk):
    limit = 13
    resp = kinopoisk.movie(query_params={
        "limit": limit
    })
    resp.check_response_code(200)
    resp.check_field_values(expected_field_values={"limit": limit})
    movies = resp.get_movies()
    with qase.step("Проверить кол-во полученных элементов", expected=f"кол-во элементов равно {limit}"):
        assert len(movies) == limit, f"кол-во элементов не равно {len(movies)} != {limit}"
