import pytest
import logging
from config import Config

_logger = logging.getLogger(__name__)


def test_config(config: Config):
    _logger.info(f"{config=}")
