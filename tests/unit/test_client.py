import pytest
from dotenv import load_dotenv

from data_bridges_knots.client import (
    DataBridgesKnots,
    config_from_env,
)


@pytest.fixture
def valid_config():
    load_dotenv()
    config = config_from_env()

    return config


@pytest.fixture
def client(valid_config):
    return DataBridgesKnots(valid_config)

def test_import():
    from data_bridges_knots.client import DataBridgesKnots

    assert DataBridgesKnots is not None


def test_deprecated_client_init(valid_config):
    client = DataBridgesKnots(valid_config)
    assert isinstance(client, DataBridgesKnots)


def test_client_init(valid_config):
    client = DataBridgesKnots(valid_config)
    assert isinstance(client, DataBridgesKnots)