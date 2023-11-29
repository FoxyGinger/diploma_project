from kinopoisk.kinopoisk import *

from qaseio.pytest import qase


@qase.id(6)
@qase.title("Получение фильмов без параметров")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie(kinopoisk: Kinopoisk):
    resp = kinopoisk.movie()
    resp.check_response_code(200)
    with qase.step("Проверить количество полученных фильмов", expected="Больше 0"):
        movies = resp.json().get('docs')
        if len(movies) <= 0:
            pytest.fail(f'В ответе нет элементов')

    with qase.step("Проверить уникальность id фильмов", expected="Уникальны"):
        ids = set([movie['id'] for movie in movies])
        if len(ids) != len(movies):
            pytest.fail(f'В ответе есть повторящиеся id')


@qase.id(296)
@qase.title("Получение выбранных полей в фильмах")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_selected_fields(kinopoisk: Kinopoisk):
    selected_fields = ['name', 'type', 'year', 'genres', 'countries', 'rating']
    resp = kinopoisk.movie(params={"selectFields": selected_fields})
    resp.check_response_code(200)
    movies = resp.json().get('docs')
    with qase.step('Проверить, что фильмы содержат только нужные поля', expected="Содержат"):
        for movie in movies:
            if set(selected_fields) != movie.keys():
                pytest.fail(f'diff fields: {set(selected_fields) ^ movie.keys()}')


@qase.id(304)
@qase.title("Получение фильмов с указанием несуществующей страницы")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "negative"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_non_existent_page(kinopoisk: Kinopoisk):
    page = 9999999
    with qase.step("Поле 'page' заполнить невалидным числом", expected=f'"page": {page}'):
        params = {"page": page}

    resp = kinopoisk.movie(params=params)
    resp.check_response_code(400)


