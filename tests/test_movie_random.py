from kinopoisk.kinopoisk import *

movie_id = 22222
invalid_movie_id = "12845%$"
invalid_token = "invalid_token"


@qase.id(30)
@qase.title("Получение рандомного тайтла из базы")
@qase.suite("Получение рандомного тайтла из базы (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_random(kinopoisk: Kinopoisk):
    resp1 = kinopoisk.movie_random()
    resp1.check_response_code(200)
    first_id = resp1.get_movies()[0].get("id")
    resp2 = kinopoisk.movie_random()
    resp2.check_response_code(200)
    second_id = resp2.get_movies()[0].get("id")
    with qase.step("Убедиться, что фильмы имеют разный id", expected="У фильмов разные id"):
        assert first_id != second_id, "У фильмов не разные id"


@qase.id(41)
@qase.title("Получение рандомного тайтла по доступным платформам для просмотра")
@qase.suite("Получение рандомного тайтла из базы (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_random_platform(kinopoisk: Kinopoisk):
    watchability_items_name = "okko"
    resp = kinopoisk.movie_random(query_params={"watchability.items.name": watchability_items_name})
    resp.check_response_code(200)
    with qase.step(f'Проверить, что фильм доступен на платформе "{watchability_items_name}"', expected=f'Фильм доступен в "{watchability_items_name}"'):
        movie = resp.get_movies()[0]
        success = False
        for current_item in movie.get("watchability").get('items'):
            if current_item.get('name') == watchability_items_name:
                success = True
                break

        assert success, f'есть фильмы не на платформе "{watchability_items_name}"'


@qase.id(34)
@qase.title("Получение рандомного тайтла по рейтингу Кинопоиск от 7 до 10")
@qase.suite("Получение рандомного тайтла из базы (фильмы, сериалы)")
@qase.fields(
    ("severity", "major"),
    ("priority", "high"),
    ("behavior", "positive"),
    ("type", "smoke"),
    ("layer", "api"),
    ("automation", "automated")
)
def test_movie_random_rating_kp_7_10(kinopoisk: Kinopoisk):
    rating_1 = 7
    rating_2 = 10
    resp = kinopoisk.movie_random(query_params={
        "rating.kp": f'{rating_1}-{rating_2}'
    })
    resp.check_response_code(200)
    movies = resp.get_movies()
    with qase.step(f'Проверить рейтинг "rating.kp" в дипозоне от {rating_1} до {rating_2}',
                   expected=f"rating.kp от {rating_1} до {rating_2}"):
        for movie in movies:
            movie_rating_kp = movie.get('rating').get('kp')
            assert rating_1 <= movie_rating_kp <= rating_2, f"рейтинг {movie_rating_kp} от {rating_1} до {rating_2}"
