import os

import pandas as pd
import pytest
from data_bridges_client.rest import ApiException

from data_bridges_knots.client import DataBridgesShapes, config_from_env
from dotenv import load_dotenv
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
    return DataBridgesShapes(config_dict)


# -------------------------
# ✅ 1. Import
# -------------------------

def test_import():
    from data_bridges_knots.client import DataBridgesShapes

    assert DataBridgesShapes is not None


# -------------------------
# ✅ 2. Config
# -------------------------


def test_client_init(config_dict):
    client = DataBridgesShapes(config_dict)
    assert isinstance(client, DataBridgesShapes)


# =========================================================
# ✅ 3. SUCCESS TESTS (expect 200)
# =========================================================


@pytest.mark.integration
@pytest.mark.parametrize(
    "func,args",
    [
        ("get_prices", ("KEN",)),
        ("get_exchange_rates", ("KEN",)),
        ("get_commodities_list", ()),
        ("get_currency_list", ()),
        ("get_markets_list", ("KEN",)),
        ("get_gorp", ("country_latest",)),
        ("get_mfi_surveys", ()),
    ],
)
def test_endpoints_success(client, func, args):
    method = getattr(client, func)

    try:
        result = method(*args)
        assert isinstance(result, (pd.DataFrame, str, bytes))
    except ApiException as e:
        pytest.fail(f"{func} returned 403 but expected success: {e}")


# =========================================================
# ✅ 4. FORBIDDEN TESTS (expect 403)
# =========================================================


@pytest.mark.integration
@pytest.mark.parametrize(
    "func,args",
    [
        ("get_household_survey", (1234, "full")),
        ("get_household_survey", (1234, "draft")),
        # Add more endpoints known to require permissions
    ],
)
def test_endpoints_forbidden(client, func, args):
    method = getattr(client, func)

    with pytest.raises(ApiException) as exc:
        method(*args)

    assert exc.value.status == 403
