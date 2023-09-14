import json
import os.path
import sys


class SchemaChecker:
    __schema_path: str
    __schemas: dict[str, dict]

    def __init__(self, schema_folder):
        self.__schema_path = f"{schema_folder}"
        self.__schemas = {}
        if not os.path.exists(self.__schema_path):
            raise ValueError(f'Response schema path do not exist "{self.__schema_path}"')

    def get_schema_data(self, schema_name: str):
        if schema_name not in self.__schemas.keys():
            self.__load_schema(schema_name)

        data = self.__schemas.get(schema_name)

        return data

    def __load_schema(self, schema_name: str):
        schema_file = f"{self.__schema_path}/{schema_name}.json"
        if not os.path.exists(self.__schema_path):
            raise ValueError(f'Schema path do not exist "{schema_file}"')

        with open(schema_file) as file:
            self.__schemas[schema_name] = json.load(file)

    def check_field_keys(self, actual_data: dict, expected_keys: [str | set]) -> bool:
        expected_fields = self.get_schema_data(expected_keys).keys() if isinstance(expected_keys, str) else expected_keys
        actual_fields = actual_data.keys()
        success = expected_fields <= actual_fields
        if not success:
            print(f'Absent fields: "{expected_fields ^ actual_fields}"', file=sys.stderr)

        return success




# sc = SchemaChecker("F:/Python/diploma_project/response_schemas", "v1")
# data = {'videos': {'trailers': [], 'teasers': []}, 'status': None, 'externalId': {'kpHD': None, 'imdb': 'tt3389706', 'tmdb': 241861}, 'rating': {'kp': 6.3, 'imdb': 7.4, 'filmCritics': 0, 'russianFilmCritics': 0, 'await': None}, 'votes': {'kp': 153, 'imdb': 1713, 'filmCritics': 0, 'russianFilmCritics': 0, 'await': 0}, 'backdrop': {'url': None, 'previewUrl': None}, 'movieLength': 11, 'images': {'framesCount': 0}, 'productionCompanies': [{'name': 'Triune Films', 'url': None, 'previewUrl': None}], 'spokenLanguages': [{'name': 'English', 'nameEn': 'English'}], 'id': 814823, 'type': 'movie', 'name': 'Близость', 'description': 'Очнувшись, несколько мужчин обнаруживают, что к их ногам привязаны бомбы, которые срабатывают, если они отходят друг от друга на большое расстояние. Им предстоит нелегкая игра на выживание…', 'distributors': {'distributor': None, 'distributorRelease': None}, 'premiere': {'world': '2013-12-05T00:00:00.000Z'}, 'slogan': None, 'year': 2013, 'poster': {'url': 'https://st.kp.yandex.net/images/film_big/814823.jpg', 'previewUrl': 'https://st.kp.yandex.net/images/film_iphone/iphone360_814823.jpg'}, 'facts': None, 'genres': [{'name': 'короткометражка'}, {'name': 'фантастика'}, {'name': 'боевик'}, {'name': 'триллер'}], 'countries': [{'name': 'США'}], 'seasonsInfo': [], 'persons': [{'id': 2681405, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2681405.jpg', 'name': 'Тодд Бруно', 'enName': 'Todd Bruno', 'description': 'Jake', 'profession': 'актеры', 'enProfession': 'actor'}, {'id': 2681422, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2681422.jpg', 'name': 'Джош Коннолли', 'enName': 'Josh Connolly', 'description': 'Luke', 'profession': 'актеры', 'enProfession': 'actor'}, {'id': 3220483, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_3220483.jpg', 'name': 'Джастин Робинсон', 'enName': 'Justin Robinson', 'description': 'Boss Hunter', 'profession': 'актеры', 'enProfession': 'actor'}, {'id': 2916903, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2916903.jpg', 'name': 'Тимоти Коннолли ст.', 'enName': 'Timothy Connolly Sr.', 'description': None, 'profession': 'актеры', 'enProfession': 'actor'}, {'id': 1899667, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_1899667.jpg', 'name': 'Дэниэл Джеймс', 'enName': 'Daniel James', 'description': None, 'profession': 'актеры', 'enProfession': 'actor'}, {'id': 2681429, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2681429.jpg', 'name': 'Тим Аллен', 'enName': 'Tim Allen', 'description': None, 'profession': 'актеры', 'enProfession': 'actor'}, {'id': 2561189, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2561189.jpg', 'name': 'Тим Коннолли мл.', 'enName': 'Tim Connolly Jr.', 'description': None, 'profession': 'актеры', 'enProfession': 'actor'}, {'id': 2681427, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2681427.jpg', 'name': None, 'enName': 'Arris Quinones', 'description': None, 'profession': 'актеры', 'enProfession': 'actor'}, {'id': 1899667, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_1899667.jpg', 'name': 'Дэниэл Джеймс', 'enName': 'Daniel James', 'description': None, 'profession': 'композиторы', 'enProfession': 'composer'}, {'id': 3465453, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_3465453.jpg', 'name': 'Эмбер Киньонес', 'enName': 'Amber Quinones', 'description': None, 'profession': 'художники', 'enProfession': 'designer'}, {'id': 2561188, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2561188.jpg', 'name': 'Райан Коннолли', 'enName': 'Ryan Connolly', 'description': None, 'profession': 'режиссеры', 'enProfession': 'director'}, {'id': 2561188, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2561188.jpg', 'name': 'Райан Коннолли', 'enName': 'Ryan Connolly', 'description': None, 'profession': 'монтажеры', 'enProfession': 'editor'}, {'id': 2561188, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2561188.jpg', 'name': 'Райан Коннолли', 'enName': 'Ryan Connolly', 'description': None, 'profession': 'операторы', 'enProfession': 'operator'}, {'id': 2681405, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2681405.jpg', 'name': 'Тодд Бруно', 'enName': 'Todd Bruno', 'description': None, 'profession': 'продюсеры', 'enProfession': 'producer'}, {'id': 2561189, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2561189.jpg', 'name': 'Тим Коннолли мл.', 'enName': 'Tim Connolly Jr.', 'description': None, 'profession': 'продюсеры', 'enProfession': 'producer'}, {'id': 2561188, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2561188.jpg', 'name': 'Райан Коннолли', 'enName': 'Ryan Connolly', 'description': None, 'profession': 'продюсеры', 'enProfession': 'producer'}, {'id': 2561188, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2561188.jpg', 'name': 'Райан Коннолли', 'enName': 'Ryan Connolly', 'description': None, 'profession': 'редакторы', 'enProfession': 'writer'}, {'id': 2544219, 'photo': 'https://st.kp.yandex.net/images/actor_iphone/iphone360_2544219.jpg', 'name': 'Сет Уорли', 'enName': 'Seth Worley', 'description': None, 'profession': 'редакторы', 'enProfession': 'writer'}], 'lists': [], 'typeNumber': 1, 'alternativeName': 'Proximity', 'enName': None, 'names': [{'name': 'Близость'}, {'name': 'Proximity'}], 'ageRating': None, 'budget': {}, 'ratingMpaa': None, 'updateDates': [], 'fees': {'world': {}, 'russia': {}, 'usa': {}}, 'updatedAt': '2023-07-03T18:07:07.569Z', 'shortDescription': None, 'technology': {'hasImax': False, 'has3D': False}, 'ticketsOnSale': False, 'sequelsAndPrequels': [], 'similarMovies': [], 'logo': {'url': None}, 'watchability': {'items': []}, 'top10': None, 'top250': None, 'deletedAt': None, 'isSeries': False, 'seriesLength': None, 'totalSeriesLength': None}
#
# res = sc.check_field_keys("movie/random", data)
# print(res)
# res = sc.check_field_keys("movie/random", data, ["externalId"])
# print(res)