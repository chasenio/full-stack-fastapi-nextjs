import os
import pytest
import argparse

from models.session import DBConnect

from config import Config
from config import load_cfg


def pytest_addoption(parser):
    class AppConfig(argparse.Action):
        def __call__(self, parser, namespace, values, option_string=None):
            if not os.path.exists(values):
                raise argparse.ArgumentError(self, f'not found {values=}')
            try:
                cfg = load_cfg(values)
                setattr(namespace, self.dest, cfg)
            except ValueError:
                raise argparse.ArgumentError(self, 'invalid yaml content')

    parser.addoption("--config", action=AppConfig, required=True, help="config file path")


@pytest.fixture(scope="session")
def config(request) -> Config:
    cfg = request.config.getoption('config')
    return cfg


@pytest.fixture(scope="session")
def db(config: Config) -> DBConnect:
    return DBConnect(db_url=config.db_url)
