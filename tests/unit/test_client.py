import pandas as pd
import pytest
from dotenv import load_dotenv

from data_bridges_knots.client import DataBridgesKnots, DataBridgesShapes, config_from_env

# -------------------------
# ✅ Fixtures
# -------------------------


@pytest.fixture
def config_dict():
    load_dotenv()
    config = config_from_env()

    return config


@pytest.fixture
def client(config_dict):
    return DataBridgesKnots(config_dict)


# -------------------------
# ✅ 1. Import
# -------------------------


def test_deprecated_import():
    from data_bridges_knots.client import DataBridgesShapes

    assert DataBridgesShapes is not None

def test_import():
    from data_bridges_knots.client import DataBridgesKnots

    assert DataBridgesKnots is not None



# -------------------------
# ✅ 2. Config
# -------------------------


def test_deprecated_client_init(config_dict):
    client = DataBridgesShapes(config_dict)
    assert isinstance(client, DataBridgesShapes)

def test_client_init(config_dict):
    client = DataBridgesKnots(config_dict)
    assert isinstance(client, DataBridgesKnots)