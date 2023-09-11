from kinopoisk.kinopoisk import Kinopoisk


def test_movie_random(kinopoisk: Kinopoisk):
    resp = kinopoisk.movie_random()
    kinopoisk.check_response_code(resp, 200)
    kinopoisk.check_response_body(resp, "movie")
