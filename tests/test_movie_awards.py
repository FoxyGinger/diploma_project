"""
Тесты для метода movie/awards
"""
from kinopoisk.kinopoisk import *


@qase.id(232)
@qase.title("Получение списка наград тайтлов без параметров")
@qase.suite("Награды тайтлов (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_awards(kinopoisk: Kinopoisk):
    """
    Получение списка наград тайтлов без параметров
    :param kinopoisk:
    :return:
    """
    award_fields = {"movieId", "nomination"}
    resp = kinopoisk.movie_awards()
    resp.check_response_code(200)
    with qase.step('Проверить, что вернулся список номинаций', expected=f'Элементы содержат поля: {award_fields}'):
        for award in resp.get_awards():
            assert award_fields <= award.keys(), f'есть элементы, которые не содержат поля: "{award_fields}"'


@qase.id(242)
@qase.title("Получение только списка наград с победами")
@qase.suite("Награды тайтлов (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_awards_winning(kinopoisk: Kinopoisk):
    """
    Получение только списка наград с победами
    :param kinopoisk:
    :return:
    """
    winning = True
    resp = kinopoisk.movie_awards(query_params={"winning": winning})
    resp.check_response_code(200)
    with qase.step(f'Проверить, что вернулся список номинаций c "winning": {winning}', expected=f'Элементы содержат поле "winning": {winning}'):
        for award in resp.get_awards():
            current_winning = award.get('winning')
            assert winning == current_winning, f'есть элементы, у которых поле "winning": {current_winning}'


@qase.id(243)
@qase.title("Получение определенного списка номинаций")
@qase.suite("Награды тайтлов (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_awards_title(kinopoisk: Kinopoisk):
    """
    Получение определенного списка номинаций
    :param kinopoisk:
    :return:
    """
    nomination_title = "Венецианский кинофестиваль"
    resp = kinopoisk.movie_awards(query_params={"nomination.title": nomination_title})
    resp.check_response_code(200)
    with qase.step(f'Проверить, что вернулся список номинаций c "nomination.title": {nomination_title}', expected=f'Элементы содержат поле "nomination.title": {nomination_title}'):
        for award in resp.get_awards():
            current_title = award.get('nomination').get('title')
            assert nomination_title == current_title, f'есть элементы, у которых поле "nomination.title": {current_title}'


@qase.id(260)
@qase.title("Получение определенного списка номинаций по наградам")
@qase.suite("Награды тайтлов (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_awards_award_title(kinopoisk: Kinopoisk):
    """
    Получение определенного списка номинаций по наградам
    :param kinopoisk:
    :return:
    """
    nomination_award_title = "Оскар"
    resp = kinopoisk.movie_awards(query_params={"nomination.award.title": nomination_award_title})
    resp.check_response_code(200)
    with qase.step(f'Проверить, что вернулся список номинаций c "nomination.award.title": {nomination_award_title}', expected=f'Элементы содержат поле "nomination.award.title": {nomination_award_title}'):
        for award in resp.get_awards():
            current_award_title = award.get('nomination').get('award').get('title')
            assert current_award_title == nomination_award_title, f'есть элементы, у которых поле "nomination.award.title": {current_award_title}'


@qase.id(261)
@qase.title("Получение определенного списка номинаций по году награды")
@qase.suite("Награды тайтлов (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_awards_award_year(kinopoisk: Kinopoisk):
    """
    Получение определенного списка номинаций по году награды
    :param kinopoisk:
    :return:
    """
    nomination_award_year = 2021
    resp = kinopoisk.movie_awards(query_params={"nomination.award.year": nomination_award_year})
    resp.check_response_code(200)
    with qase.step(f'Проверить, что вернулся список номинаций c "nomination.award.year": {nomination_award_year}', expected=f'Элементы содержат поле "nomination.award.year": {nomination_award_year}'):
        for award in resp.get_awards():
            current_award_year = award.get('nomination').get('award').get('year')
            assert current_award_year == nomination_award_year, f'есть элементы, у которых поле "nomination.award.year": {current_award_year}'


@qase.id(328)
@qase.title("Получение определенного списка номинаций по году награды 1900")
@qase.suite("Награды тайтлов (фильмы, сериалы)")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "positive"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_awards_award_year_1900(kinopoisk: Kinopoisk):
    """
    Получение определенного списка номинаций по году награды 1900
    :param kinopoisk:
    :return:
    """
    nomination_award_year = 1900
    resp = kinopoisk.movie_awards(query_params={"nomination.award.year": nomination_award_year})
    resp.check_response_code(200)
    with qase.step(f'Проверить, что вернулся список номинаций c "nomination.award.year": {nomination_award_year}', expected=f'Элементы содержат поле "nomination.award.year": {nomination_award_year}'):
        for award in resp.get_awards():
            current_award_year = award.get('nomination').get('award').get('year')
            assert current_award_year == nomination_award_year, f'есть элементы, у которых поле "nomination.award.year": {current_award_year}'


@qase.id(329)
@qase.title("Получение определенного списка номинаций по году награды 1899")
@qase.suite("Награды тайтлов (фильмы, сериалы)")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "negative"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_awards_award_year_1899(kinopoisk: Kinopoisk):
    """
    Получение определенного списка номинаций по году награды 1899
    :param kinopoisk:
    :return:
    """
    nomination_award_year = 1899
    resp = kinopoisk.movie_awards(query_params={"nomination.award.year": nomination_award_year})
    resp.check_response_code(400)


@qase.id(330)
@qase.title("Получение определенного списка номинаций по году награды 3333")
@qase.suite("Награды тайтлов (фильмы, сериалы)")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "negative"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_awards_award_year_3333(kinopoisk: Kinopoisk):
    """
    Получение определенного списка номинаций по году награды 3333
    :param kinopoisk:
    :return:
    """
    nomination_award_year = 3333
    resp = kinopoisk.movie_awards(query_params={"nomination.award.year": nomination_award_year})
    resp.check_response_code(400)
