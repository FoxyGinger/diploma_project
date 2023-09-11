import os
import sys

import pytest
import yaml

from kinopoisk.kinopoisk import Kinopoisk

config_file = "config.yaml"


@pytest.fixture()
def config() -> dict:
    os.chdir(os.path.dirname(__file__))
    config: dict = {}
    if not os.path.exists(config_file):
        print(f'Warning! Config file "{config_file}" is not exists', file=sys.stderr)

    with open(config_file) as file:
        config = yaml.load(file, Loader=yaml.loader.SafeLoader)

    if len(config) == 0:
        raise ValueError(f'Config is invalid! Check config file "{config_file}"')

    yield config


@pytest.fixture()
def kinopoisk(config: dict) -> Kinopoisk:
    kinopoisk = Kinopoisk(config)
    yield kinopoisk

