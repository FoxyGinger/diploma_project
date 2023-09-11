import json
import os.path
import sys


class SchemaChecker:
    __schema_path: str
    __schemas: dict[str, dict]

    def __init__(self, schema_folder, api_version):
        self.__schema_path = f"{schema_folder}/{api_version}"
        self.__schemas = {}
        if not os.path.exists(self.__schema_path):
            raise ValueError(f'Response schema path do not exist "{self.__schema_path}"')

    def __get_schema_data(self, schema_name: str, nested_keys: list = None):
        if schema_name not in self.__schemas.keys():
            self.__get_schema(schema_name)

        data = self.__schemas.get(schema_name)
        if nested_keys is not None:
            data = self.__get_nested_data(data, nested_keys)

        return data

    def __get_nested_data(self, data: dict, nested_keys: list) -> dict:
        nested_keys_tmp = [value for value in nested_keys]
        while len(nested_keys_tmp) != 0:
            data = data.get(nested_keys_tmp.pop(0))

        return data

    def check_field_keys(self, schema_name: str, data: dict, nested_keys: list = None) -> bool:
        if schema_name not in self.__schemas.keys():
            self.__get_schema(schema_name)

        expected_fields = self.__get_schema_data(schema_name, nested_keys).keys()
        actual_fields = data.keys() if nested_keys is None else self.__get_nested_data(data, nested_keys).keys()
        success = expected_fields <= actual_fields
        if not success:
            print(f'Absent fields of "{schema_name}" : "{actual_fields ^ expected_fields}"', file=sys.stderr)

        return success

    def __get_schema(self, schema_name: str):
        schema_file = f"{self.__schema_path}/{schema_name}.json"
        if not os.path.exists(self.__schema_path):
            raise ValueError(f'Schema path do not exist "{schema_file}"')

        with open(schema_file) as file:
            self.__schemas[schema_name] = json.load(file)


# sc = SchemaChecker("F:/Python/diploma_project/response_schemas", "v1")
# data = {
#   "id": 666,
#   "externalId": {
#     "kpHD": "48e8d0acb0f62d8585101798eaeceec5",
#     "imdb": "tt0232500",
#     "tmdb": 9799
#   },
#   "name": "Человек паук",
#   "alternativeName": "Spider man",
#   "enName": "Spider man",
#   "names": [
#     {
#       "name": "string",
#       "language": "string",
#       "type": "string"
#     }
#   ],
#   "type": "movie",
#   "typeNumber": 1,
#   "year": 2023,
#   "description": "string",
#   "shortDescription": "string",
#   "slogan": "string",
#   "status": "completed",
#   "rating": {
#     "kp": 6.2,
#     "imdb": 8.4,
#     "tmdb": 3.2,
#     "filmCritics": 10,
#     "russianFilmCritics": 5.1,
#     "await": 6.1
#   },
#   "votes": {
#     "kp": "60000",
#     "imdb": "50000",
#     "tmdb": 10000,
#     "filmCritics": 10000,
#     "russianFilmCritics": 4000,
#     "await": 34000
#   },
#   "movieLength": 120,
#   "ratingMpaa": "pg13",
#   "ageRating": 16,
#   "logo": {
#     "url": "string"
#   },
#   "poster": {
#     "url": "string",
#     "previewUrl": "string"
#   },
#   "backdrop": {
#     "url": "string",
#     "previewUrl": "string"
#   },
#   "videos": {
#     "trailers": [
#       {
#         "url": "https://www.youtube.com/embed/ZsJz2TJAPjw",
#         "name": "Official Trailer",
#         "site": "youtube",
#         "type": "TRAILER",
#         "size": 0
#       }
#     ],
#     "teasers": [
#       {
#         "url": "https://www.youtube.com/embed/ZsJz2TJAPjw",
#         "name": "Official Trailer",
#         "site": "youtube",
#         "type": "TRAILER",
#         "size": 0
#       }
#     ]
#   },
#   "genres": [
#     {
#       "name": "string"
#     }
#   ],
#   "countries": [
#     {
#       "name": "string"
#     }
#   ],
#   "persons": [
#     {
#       "id": 6317,
#       "photo": "https://st.kp.yandex.net/images/actor_iphone/iphone360_6317.jpg",
#       "name": "Пол Уокер",
#       "enName": "Paul Walker",
#       "description": "string",
#       "profession": "string",
#       "enProfession": "string"
#     }
#   ],
#   "reviewInfo": {
#     "count": 0,
#     "positiveCount": 0,
#     "percentage": "string"
#   },
#   "seasonsInfo": [
#     {
#       "number": 0,
#       "episodesCount": 0
#     }
#   ],
#   "budget": {
#     "value": 207283,
#     "currency": "€"
#   },
#   "fees": {
#     "world": {
#       "value": 207283,
#       "currency": "€"
#     },
#     "russia": {
#       "value": 207283,
#       "currency": "€"
#     },
#     "usa": {
#       "value": 207283,
#       "currency": "€"
#     }
#   },
#   "premiere": {
#     "country": "США",
#     "world": "2023-02-25T02:44:39.359Z",
#     "russia": "2023-02-25T02:44:39.359Z",
#     "digital": "string",
#     "cinema": "2023-02-25T02:44:39.359Z",
#     "bluray": "string",
#     "dvd": "string"
#   },
#   "similarMovies": [
#     {
#       "id": 0,
#       "name": "string",
#       "enName": "string",
#       "alternativeName": "string",
#       "type": "string",
#       "poster": {
#         "url": "string",
#         "previewUrl": "string"
#       }
#     }
#   ],
#   "sequelsAndPrequels": [
#     {
#       "id": 0,
#       "name": "string",
#       "enName": "string",
#       "alternativeName": "string",
#       "type": "string",
#       "poster": {
#         "url": "string",
#         "previewUrl": "string"
#       }
#     }
#   ],
#   "watchability": {
#     "items": [
#       {
#         "name": "string",
#         "logo": {
#           "url": "string"
#         },
#         "url": "string"
#       }
#     ]
#   },
#   "releaseYears": [
#     {
#       "start": 2022,
#       "end": 2023
#     }
#   ],
#   "top10": 1,
#   "top250": 200,
#   "ticketsOnSale": True,
#   "totalSeriesLength": 155,
#   "seriesLength": 20,
#   "isSeries": True,
#   "audience": [
#     {
#       "count": 1000,
#       "country": "Россия"
#     }
#   ],
#   "facts": [
#     {
#       "value": "string",
#       "type": "string",
#       "spoiler": True
#     }
#   ],
#   "imagesInfo": {
#     "postersCount": 0,
#     "backdropsCount": 0,
#     "framesCount": 0
#   },
#   "productionCompanies": [
#     {
#       "name": "string",
#       "url": "string",
#       "previewUrl": "string"
#     }
#   ]
# }
#
# res = sc.check_field_keys("movie", data, ["imagesInfo"])
# print(res)
# res = sc.check_field_keys("movie", data)
# print(res)