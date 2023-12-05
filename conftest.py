"""
Файл содержит основные фикстуры для тестов
"""
import os
import sys

import pytest
import yaml

from kinopoisk.kinopoisk import Kinopoisk

CONFIG_FILE = "config.yaml"


@pytest.fixture()
def config() -> dict:
    """
    Фикстура представляет собой словарь с параметрами для тестов
    """
    os.chdir(os.path.dirname(__file__))
    cfg: dict = {}
    if not os.path.exists(CONFIG_FILE):
        print(f'Warning! Config file "{CONFIG_FILE}" is not exists', file=sys.stderr)

    with open(CONFIG_FILE, encoding="utf-8") as file:
        cfg = yaml.safe_load(file)

    if len(cfg) == 0:
        raise ValueError(f'Config is invalid! Check config file "{CONFIG_FILE}"')

    yield cfg


@pytest.fixture()
def kinopoisk(config: dict) -> Kinopoisk:
    """
    Фикстура представляет собой объект класса Kinopoisk
    """
    kp = Kinopoisk(config)
    yield kp
