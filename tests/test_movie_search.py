"""
Тесты для метода movie/search
"""
from kinopoisk.kinopoisk import *


@qase.id(26)
@qase.title("Получение фильма по названию на русском")
@qase.suite("Поиск фильмов по названию (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_search_ru(kinopoisk: Kinopoisk):
    """
    Получение фильма по названию на русском
    :param kinopoisk:
    :return:
    """
    text = "гром"
    resp = kinopoisk.movie_search(text=text)
    resp.check_response_code(200)
    with qase.step(f'Проверить в названих фильмов содержится текст "{text}"', expected='Текст содержится'):
        for movie in resp.get_movies():
            success = False
            for current_name in movie.get('names'):
                if text in current_name.get('name').lower():
                    success = True
                    break

            assert success, f'есть фильмы, которые не содержится текст "{text}"'


@qase.id(327)
@qase.title("Получение фильма по названию на английском")
@qase.suite("Поиск фильмов по названию (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_search_eng(kinopoisk: Kinopoisk):
    """
    Получение фильма по названию на английском
    :param kinopoisk:
    :return:
    """
    text = "war"
    resp = kinopoisk.movie_search(text=text)
    resp.check_response_code(200)
    with qase.step(f'Проверить в названих фильмов содержится текст "{text}"', expected='Текст содержится'):
        for movie in resp.get_movies():
            success = False
            for current_name in movie.get('names'):
                if text in current_name.get('name').lower():
                    success = True
                    break

            assert success, f'есть фильмы, которые не содержится текст "{text}"'


