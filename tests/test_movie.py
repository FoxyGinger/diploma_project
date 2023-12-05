"""
Тесты для метода movie
"""
from kinopoisk.kinopoisk import *

FIRST_YEAR = 1874
LAST_YEAR = 2050


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
    """
    Получение фильмов без параметров
    :param kinopoisk:
    :return:
    """
    resp = kinopoisk.movie()
    resp.check_response_code(200)
    movies = resp.get_movies()
    with qase.step("Проверить количество полученных фильмов", expected="Больше 0"):
        assert len(movies) > 0, "Фильмов нет"

    with qase.step("Проверить уникальность id фильмов", expected="Уникальны"):
        ids = set(movie['id'] for movie in movies)
        assert len(ids) == len(movies), 'В ответе есть повторящиеся id'


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
    """
    Получение выбранных полей в фильмах
    :param kinopoisk:
    :return:
    """
    selected_fields = ['name', 'type', 'year', 'genres', 'countries', 'rating']
    resp = kinopoisk.movie(query_params={"selectFields": selected_fields})
    resp.check_response_code(200)
    movies = resp.get_movies()
    with qase.step('Проверить, что фильмы содержат только нужные поля', expected="Содержат"):
        for movie in movies:
            assert set(
                selected_fields) == movie.keys(), f"Содержаться другие поля: {set(selected_fields) ^ movie.keys()}"


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
    """
    Получение фильмов с указанием несуществующей страницы
    :param kinopoisk:
    :return:
    """
    page = 9999999
    resp = kinopoisk.movie(query_params={"page": page})
    resp.check_response_code(400)


@qase.id(13)
@qase.title("Получение фильмов с сортировкой по году по возрастанию")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_sort_year_asc(kinopoisk: Kinopoisk):
    """
    Получение фильмов с сортировкой по году по возрастанию
    :param kinopoisk:
    :return:
    """
    resp = kinopoisk.movie(query_params={
        "sortField": "year",
        "sortType": 1,
        "notNullFields": "year"})
    resp.check_response_code(200)
    movies = resp.get_movies()
    year = movies[0].get('year')
    with qase.step('Проверить сортировку по возрастанию по полю "year"', expected="year идут по возрастанию"):
        with qase.step("Проверить, что года ненулевые", expected="Года ненулевые"):
            pass

        for movie in movies[1:]:
            current_movie_year = movie.get('year')
            assert year > 0, "год нулевой"
            assert year <= current_movie_year, "года идут не по возрастанию"
            year = current_movie_year


@qase.id(14)
@qase.title("Получение фильмов с сортировкой по году по убыванию")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_sort_year_desc(kinopoisk: Kinopoisk):
    """
    Получение фильмов с сортировкой по году по убыванию
    :param kinopoisk:
    :return:
    """
    resp = kinopoisk.movie(query_params={
        "sortField": "year",
        "sortType": -1,
        "notNullFields": "year"})
    resp.check_response_code(200)
    movies = resp.get_movies()
    year = movies[0].get('year')
    with qase.step('Проверить сортировку по убыванию по полю "year"', expected="year идут по убыванию"):
        with qase.step("Проверить, что года ненулевые", expected="Года ненулевые"):
            pass

        for movie in movies[1:]:
            current_movie_year = movie.get('year')
            assert year > 0, "год нулевой"
            assert year >= current_movie_year, "года идут не по убыванию"
            year = current_movie_year


@qase.id(15)
@qase.title("Получение фильмов с сортировкой по рейтингу Кинопоиск по возрастанию из топ-10")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_sort_rating_kp_asc(kinopoisk: Kinopoisk):
    """
    Получение фильмов с сортировкой по рейтингу Кинопоиск по возрастанию из топ-10
    :param kinopoisk:
    :return:
    """
    resp = kinopoisk.movie(query_params={
        "sortField": "rating.kp",
        "sortType": 1,
        "notNullFields": "top10"})
    resp.check_response_code(200)
    movies = resp.get_movies()
    rating_kp = movies[0].get('rating').get('kp')
    with qase.step('Проверить сортировку по возрастанию по полю "rating.kp"', expected="rating.kp идут по возрастанию"):
        for movie in movies[1:]:
            current_movie_rating_kp = movie.get('rating').get('kp')
            assert rating_kp <= current_movie_rating_kp, "рейтинги идут не по возрастанию"
            rating_kp = current_movie_rating_kp


@qase.id(16)
@qase.title("Получение фильмов с сортировкой по рейтингу Кинопоиск по убыванию из топ-10")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_sort_rating_kp_desc(kinopoisk: Kinopoisk):
    """
    Получение фильмов с сортировкой по рейтингу Кинопоиск по убыванию из топ-10
    :param kinopoisk:
    :return:
    """
    resp = kinopoisk.movie(query_params={
        "sortField": "rating.kp",
        "sortType": -1,
        "notNullFields": "top10"})
    resp.check_response_code(200)
    movies = resp.get_movies()
    rating_kp = movies[0].get('rating').get('kp')
    with qase.step('Проверить сортировку по убыванию по полю "rating.kp"', expected="rating.kp идут по возрастанию"):
        for movie in movies[1:]:
            current_movie_rating_kp = movie.get('rating').get('kp')
            assert rating_kp >= current_movie_rating_kp, "рейтинги идут не по убыванию"
            rating_kp = current_movie_rating_kp


@qase.id(18)
@qase.title("Получение фильмов по году с нижней границы")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_valid_first_year(kinopoisk: Kinopoisk):
    """
    Получение фильмов по году с нижней границы
    :param kinopoisk:
    :return:
    """
    resp = kinopoisk.movie(query_params={
        "year": FIRST_YEAR})
    resp.check_response_code(200)
    movies = resp.get_movies()
    with qase.step(f'Проверить, что год в фильмах равен {FIRST_YEAR}', expected=f"Все фильмы {FIRST_YEAR} года"):
        for movie in movies:
            year = movie.get('year')
            assert year == FIRST_YEAR, f"{year} != {FIRST_YEAR}"


@qase.id(19)
@qase.title("Получение фильмов по году с верхней границы")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_valid_last_year(kinopoisk: Kinopoisk):
    """
    Получение фильмов по году с верхней границы
    :param kinopoisk:
    :return:
    """
    resp = kinopoisk.movie(query_params={
        "year": LAST_YEAR})
    resp.check_response_code(200)
    movies = resp.get_movies()
    with qase.step(f'Проверить, что год в фильмах равен {LAST_YEAR}', expected=f"Все фильмы {LAST_YEAR} года"):
        for movie in movies:
            year = movie.get('year')
            assert year == LAST_YEAR, f"{year} != {LAST_YEAR}"


@qase.id(314)
@qase.title("Получение фильмов по году с нижней границы + 1")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_valid_first_year_1(kinopoisk: Kinopoisk):
    """
    Получение фильмов по году с нижней границы + 1
    :param kinopoisk:
    :return:
    """
    valid_year = FIRST_YEAR + 1
    resp = kinopoisk.movie(query_params={
        "year": valid_year})
    resp.check_response_code(200)
    movies = resp.get_movies()
    with qase.step(f'Проверить, что год в фильмах равен {valid_year}', expected=f"Все фильмы {valid_year} года"):
        for movie in movies:
            year = movie.get('year')
            assert year == valid_year, f"{year} != {valid_year}"


@qase.id(315)
@qase.title("Получение фильмов по году с верхней границы - 1")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_valid_last_year_1(kinopoisk: Kinopoisk):
    """
    Получение фильмов по году с верхней границы - 1
    :param kinopoisk:
    :return:
    """
    valid_year = LAST_YEAR - 1
    resp = kinopoisk.movie(query_params={
        "year": valid_year})
    resp.check_response_code(200)
    movies = resp.get_movies()
    with qase.step(f'Проверить, что год в фильмах равен {valid_year}', expected=f"Все фильмы {valid_year} года"):
        for movie in movies:
            year = movie.get('year')
            assert year == valid_year, f"{year} != {valid_year}"


@qase.id(20)
@qase.title("Получение фильмов по году за нижней границей")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "negative"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_invalid_first_year(kinopoisk: Kinopoisk):
    """
    Получение фильмов по году за нижней границей
    :param kinopoisk:
    :return:
    """
    invalid_year = FIRST_YEAR - 1
    resp = kinopoisk.movie(query_params={
        "year": invalid_year})
    resp.check_response_code(400)


@qase.id(22)
@qase.title("Получение фильмов по году за верхней границей")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "negative"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_invalid_last_year(kinopoisk: Kinopoisk):
    """
    Получение фильмов по году за верхней границей
    :param kinopoisk:
    :return:
    """
    invalid_year = LAST_YEAR + 1
    resp = kinopoisk.movie(query_params={
        "year": invalid_year})
    resp.check_response_code(400)


@qase.id(23)
@qase.title("Получение фильмов по жанрам")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_by_genre(kinopoisk: Kinopoisk):
    """
    Получение фильмов по жанрам
    :param kinopoisk:
    :return:
    """
    genre = "комедия"
    resp = kinopoisk.movie(query_params={
        "genre.name": genre})
    resp.check_response_code(200)
    with qase.step(f'Проверить, что фильмы принадлежат жанру "{genre}"', expected=f'Все фильмы жанра "{genre}"'):
        movies = resp.get_movies()
        for movie in movies:
            success = False
            for current_genre in movie.get('genres'):
                if current_genre.get('name') == genre:
                    success = True
                    break

            assert success, f'есть фильмы не жанра "{genre}"'


@qase.id(316)
@qase.title("Получение фильмов по нескольким жанрам")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_by_two_genres(kinopoisk: Kinopoisk):
    """
    Получение фильмов по нескольким жанрам
    :param kinopoisk:
    :return:
    """
    genre1 = "комедия"
    genre2 = "криминал"
    resp = kinopoisk.movie(query_params={
        "genre.name": [f'+{genre1}', f'+{genre2}']})
    resp.check_response_code(200)
    with qase.step(f'Проверить, что фильмы принадлежат жанру "{genre1}" и "{genre2}"',
                   expected=f'Все фильмы жанра "{genre1}" и "{genre2}"'):
        movies = resp.get_movies()
        for movie in movies:
            success1 = False
            success2 = False
            for current_genre in movie.get('genres'):
                if current_genre.get('name') == genre1:
                    success1 = True
                elif current_genre.get('name') == genre2:
                    success2 = True

                if success1 and success2:
                    break

            assert success1 and success2, f'есть фильмы не жанра "{genre1}" и "{genre2}"'


@qase.id(317)
@qase.title("Получение фильмов по жанру и исключающему жанру")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_by_two_genres_ex(kinopoisk: Kinopoisk):
    """
    Получение фильмов по жанру и исключающему жанру
    :param kinopoisk:
    :return:
    """
    genre1 = "комедия"
    genre2 = "криминал"
    resp = kinopoisk.movie(query_params={
        "genre.name": [f'+{genre1}', f'!{genre2}']})
    resp.check_response_code(200)
    with qase.step(f'Проверить, что фильмы принадлежат жанру "{genre1}" и не "{genre2}"',
                   expected=f'Все фильмы жанра "{genre1}" и не "{genre2}"'):
        movies = resp.get_movies()
        for movie in movies:
            success1 = False
            success2 = True
            for current_genre in movie.get('genres'):
                if current_genre.get('name') == genre1:
                    success1 = True
                elif current_genre.get('name') == genre2:
                    success2 = False
                    break

            assert success1 and success2, f'есть фильмы не жанра "{genre1}" и "{genre2}"'


@qase.id(318)
@qase.title("Получение фильмов по рейтингу Кинопоиска от 0 до 10")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_rating_kp_0_10(kinopoisk: Kinopoisk):
    """
    Получение фильмов по рейтингу Кинопоиска от 0 до 10
    :param kinopoisk:
    :return:
    """
    rating_1 = 0
    rating_2 = 10
    resp = kinopoisk.movie(query_params={
        "rating.kp": f'{rating_1}-{rating_2}'
    })
    resp.check_response_code(200)
    movies = resp.get_movies()
    with qase.step(f'Проверить рейтинг "rating.kp" в дипозоне от {rating_1} до {rating_2}',
                   expected=f"rating.kp от {rating_1} до {rating_2}"):
        for movie in movies:
            movie_rating_kp = movie.get('rating').get('kp')
            assert rating_1 <= movie_rating_kp <= rating_2, f"рейтинг {movie_rating_kp} от {rating_1} до {rating_2}"


@qase.id(319)
@qase.title("Получение фильмов по рейтингу Кинопоиска от 1 до 5")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_rating_kp_1_5(kinopoisk: Kinopoisk):
    """
    Получение фильмов по рейтингу Кинопоиска от 1 до 5
    :param kinopoisk:
    :return:
    """
    rating_1 = 1
    rating_2 = 5
    resp = kinopoisk.movie(query_params={
        "rating.kp": f'{rating_1}-{rating_2}'
    })
    resp.check_response_code(200)
    movies = resp.get_movies()
    with qase.step(f'Проверить рейтинг "rating.kp" в дипозоне от {rating_1} до {rating_2}',
                   expected=f"rating.kp от {rating_1} до {rating_2}"):
        for movie in movies:
            movie_rating_kp = movie.get('rating').get('kp')
            assert rating_1 <= movie_rating_kp <= rating_2, f"рейтинг {movie_rating_kp} от {rating_1} до {rating_2}"


@qase.id(320)
@qase.title("Получение фильмов по рейтингу Кинопоиска от 9 до 10")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_rating_kp_9_10(kinopoisk: Kinopoisk):
    """
    Получение фильмов по рейтингу Кинопоиска от 9 до 10
    :param kinopoisk:
    :return:
    """
    rating_1 = 9
    rating_2 = 10
    resp = kinopoisk.movie(query_params={
        "rating.kp": f'{rating_1}-{rating_2}'
    })
    resp.check_response_code(200)
    movies = resp.get_movies()
    with qase.step(f'Проверить рейтинг "rating.kp" в дипозоне от {rating_1} до {rating_2}',
                   expected=f"rating.kp от {rating_1} до {rating_2}"):
        for movie in movies:
            movie_rating_kp = movie.get('rating').get('kp')
            assert rating_1 <= movie_rating_kp <= rating_2, f"рейтинг {movie_rating_kp} от {rating_1} до {rating_2}"


@qase.id(321)
@qase.title("Получение фильмов по рейтингу Кинопоиска 10")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "negative"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_rating_kp_10(kinopoisk: Kinopoisk):
    """
    Получение фильмов по рейтингу Кинопоиска 10
    :param kinopoisk:
    :return:
    """
    rating = 10
    resp = kinopoisk.movie(query_params={
        "rating.kp": rating
    })
    resp.check_response_code(200)
    movies = resp.get_movies()
    with qase.step(f'Проверить рейтинг "rating.kp" равен {rating}', expected=f"rating.kp равен {rating}"):
        for movie in movies:
            movie_rating_kp = movie.get('rating').get('kp')
            assert rating == movie_rating_kp, f"рейтинг {movie_rating_kp} != {rating}"


@qase.id(322)
@qase.title("Получение фильмов по рейтингу Кинопоиска от 10 до 11")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "negative"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_rating_kp_10_11(kinopoisk: Kinopoisk):
    """
    Получение фильмов по рейтингу Кинопоиска от 10 до 11
    :param kinopoisk:
    :return:
    """
    rating_1 = 10
    rating_2 = 11
    resp = kinopoisk.movie(query_params={
        "rating.kp": f'{rating_1}-{rating_2}'
    })
    resp.check_response_code(400)


@qase.id(323)
@qase.title("Получение фильмов по рейтингу Кинопоиска от -1 до 0")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "negative"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_rating_kp_1_0(kinopoisk: Kinopoisk):
    """
    Получение фильмов по рейтингу Кинопоиска от -1 до 0
    :param kinopoisk:
    :return:
    """
    rating_1 = -1
    rating_2 = 0
    resp = kinopoisk.movie(query_params={
        "rating.kp": f'{rating_1}-{rating_2}'
    })
    resp.check_response_code(400)


@qase.id(17)
@qase.title("Получение фильмов по типу фильма с валидным значением")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_by_type(kinopoisk: Kinopoisk):
    """
    Получение фильмов по типу фильма с валидным значением
    :param kinopoisk:
    :return:
    """
    movie_type = "cartoon"
    resp = kinopoisk.movie(query_params={
        "type": movie_type
    })
    resp.check_response_code(200)
    movies = resp.get_movies()
    with qase.step(f'Проверить тип "type" равен {movie_type}', expected=f"type равен {movie_type}"):
        for movie in movies:
            current_movie_type = movie.get('type')
            assert current_movie_type == movie_type, f"type {current_movie_type} != {movie_type}"


@qase.id(306)
@qase.title("Получение фильмов по типу с невалидным значением")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "negative"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_by_invalid_type(kinopoisk: Kinopoisk):
    """
    Получение фильмов по типу с невалидным значением
    :param kinopoisk:
    :return:
    """
    movie_type = "телесериал"
    resp = kinopoisk.movie(query_params={
        "type": movie_type
    })
    resp.check_response_code(400)


@qase.id(326)
@qase.title("Получение фильмов по стране")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_by_country(kinopoisk: Kinopoisk):
    """
    Получение фильмов по стране
    :param kinopoisk:
    :return:
    """
    country_name = "Россия"
    resp = kinopoisk.movie(query_params={
        "countries.name": country_name
    })
    resp.check_response_code(200)
    with qase.step(f'Проверить, что фильмы относятся к стране "{country_name}"',
                   expected=f'Все фильмы страны "{country_name}"'):
        movies = resp.get_movies()
        for movie in movies:
            success = False
            for current_country_name in movie.get('countries'):
                if current_country_name.get('name') == country_name:
                    success = True
                    break

            assert success, f'есть фильмы не страны "{country_name}"'


@qase.id(300)
@qase.title("Получение фильмов по возрастному рейтингу")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_by_age(kinopoisk: Kinopoisk):
    """
    Получение фильмов по возрастному рейтингу
    :param kinopoisk:
    :return:
    """
    age_rating = 6
    resp = kinopoisk.movie(query_params={
        "ageRating": age_rating
    })
    resp.check_response_code(200)
    with qase.step(f'Проверить, что фильмы относятся к возрастному рейтингу "{age_rating}"',
                   expected=f'Все фильмы с возрастным рейтингом не выше "{age_rating}"'):
        movies = resp.get_movies()
        for movie in movies:
            current_age_rating = movie.get('ageRating')

            assert current_age_rating <= age_rating, f'есть фильмы c возрастным рейтингом: {current_age_rating}'


@qase.id(21)
@qase.title("Получение фильмов по продолжительности фильма от 70 до 90 мин")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_by_duration_70_90(kinopoisk: Kinopoisk):
    """
    Получение фильмов по продолжительности фильма от 70 до 90 мин
    :param kinopoisk:
    :return:
    """
    duration_first = 70
    duration_last = 90
    resp = kinopoisk.movie(query_params={
        "movieLength": f"{duration_first}-{duration_last}"
    })
    resp.check_response_code(200)
    with qase.step(f'Проверить, что у фильмов продолжительность от {duration_first} до {duration_last} мин',
                   expected='У всех фильмов продолжительность попадает в диапазон'):
        movies = resp.get_movies()
        for movie in movies:
            current_duration = movie.get('movieLength')

            assert duration_first <= current_duration <= duration_last, f'есть фильмы с продолжительностью: {current_duration}'


@qase.id(331)
@qase.title("Получение фильмов по продолжительности фильма -1")
@qase.suite("Поиск фильма с фильтрами (фильмы, сериалы)")
@qase.fields(
    ("severity", "normal"),
    ("priority", "medium"),
    ("behavior", "negative"),
    ("type", "regression"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_by_duration_negative(kinopoisk: Kinopoisk):
    """
    Получение фильмов по продолжительности фильма -1
    :param kinopoisk:
    :return:
    """
    duration = -1
    resp = kinopoisk.movie(query_params={
        "movieLength": duration
    })
    resp.check_response_code(400)
