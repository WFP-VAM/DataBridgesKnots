import pandas as pd
import pytest
from dotenv import load_dotenv

from data_bridges_knots.client import (
    DataBridgesKnots,
    config_from_env,
)

pytestmark = pytest.mark.integration


# =========================================================
# ✅ 3. SUCCESS TESTS (expect 200)
# =========================================================


@pytest.fixture
def valid_config():
    load_dotenv()
    config = config_from_env()

    return config


@pytest.fixture
def client(valid_config):
    return DataBridgesKnots(valid_config)


# =========================================================
# ✅ PRICES & CURRENCY
# =========================================================


@pytest.mark.integration
@pytest.mark.parametrize(
    "func,args,kwargs",
    [
        # Prices
        ("get_prices", ("KEN",), {}),
        (
            "get_prices",
            ("KEN",),
            {"start_date": "2025-01-01", "end_date": "2025-12-31"},
        ),
        # Exchange rates
        ("get_exchange_rates", ("ETH",), {}),
        # Currency
        ("get_currency_list", (), {"country_iso3": "TZA"}),
        ("get_currency_list", (), {"currency_name": "ETB"}),
        ("get_currency_list", (), {"currency_id": 1}),
        # USD indirect quotation
        ("get_usd_indirect_quotation", (), {"country_iso3": "ETH"}),
        ("get_usd_indirect_quotation", (), {"currency_name": "ETB"}),
    ],
)
def test_prices_and_currency_endpoints(client, func, args, kwargs):
    method = getattr(client, func)
    result = method(*args, **kwargs)
    assert isinstance(result, (pd.DataFrame, str, bytes))


# =========================================================
# ✅ COMMODITIES
# =========================================================


@pytest.mark.integration
@pytest.mark.parametrize(
    "func,args,kwargs",
    [
        # Commodities
        ("get_commodities_list", (), {}),
        ("get_commodities_list", (), {"country_iso3": "TZA"}),
        ("get_commodities_list", (), {"commodity_name": "Maize"}),
        ("get_commodities_list", (), {"commodity_id": 123}),
        # Commodity units
        ("get_commodity_units_list", (), {"country_iso3": "TZA"}),
        ("get_commodity_units_list", (), {"commodity_unit_name": "Kg"}),
        ("get_commodity_units_list", (), {"commodity_unit_id": 5}),
        # Commodity conversions
        ("get_commodity_units_conversion_list", (), {}),
        ("get_commodity_units_conversion_list", (), {"country_iso3": "TZA"}),
        # Commodity categories
        ("get_commodity_categories_list", (), {"country_iso3": "AFG"}),
    ],
)
def test_commodities_endpoints(client, func, args, kwargs):
    method = getattr(client, func)
    result = method(*args, **kwargs)
    assert isinstance(result, (pd.DataFrame, str, bytes))


# =========================================================
# ✅ MARKETS
# =========================================================


@pytest.mark.integration
@pytest.mark.parametrize(
    "func,args,kwargs",
    [
        ("get_markets_list", ("AFG",), {}),
        ("get_markets_as_csv", ("AFG",), {}),
        ("get_markets_as_csv", ("AFG",), {"local_names": True}),
        ("get_nearby_markets", ("AFG", 34.515, 69.208), {}),
    ],
)
def test_markets_endpoints(client, func, args, kwargs):
    method = getattr(client, func)
    result = method(*args, **kwargs)
    assert isinstance(result, (pd.DataFrame, str, bytes))


# =========================================================
# ✅ GEOJSON
# =========================================================


@pytest.mark.integration
@pytest.mark.parametrize(
    "func,args,kwargs",
    [
        ("get_market_geojson_list", ("AFG",), {}),
    ],
)
def test_geojson_endpoints(client, func, args, kwargs):
    method = getattr(client, func)
    result = method(*args, **kwargs)
    assert isinstance(result, dict)


# =========================================================
# ✅ ECONOMIC + OUTLOOK
# =========================================================


@pytest.mark.integration
@pytest.mark.parametrize(
    "func,args,kwargs",
    [
        ("get_economic_indicator_list", (), {}),
    ],
)
def test_economic_indicator_endpoints(client, func, args, kwargs):
    method = getattr(client, func)
    result = method(*args, **kwargs)
    assert isinstance(result, (pd.DataFrame, str, bytes))


# =========================================================
# ✅ HOUSEHOLD & SURVEYS
# =========================================================


@pytest.mark.integration
@pytest.mark.parametrize(
    "func,args,kwargs",
    [
        ("get_household_survey", (3094, "official"), {}),
        ("get_household_survey", (3094, "public"), {}),
        (
            "get_household_surveys_list",
            (),
            {
                "country_iso3": "COG",
                "start_date": "2024-01-01",
                "end_date": "2024-12-31",
            },
        ),
        ("get_household_xlsform_definition", (2067,), {}),
        ("get_household_questionnaire", (2075,), {}),
        ("get_choice_list", (123,), {}),
    ],
)
def test_household_endpoints(client, func, args, kwargs):
    method = getattr(client, func)
    result = method(*args, **kwargs)
    assert isinstance(result, (pd.DataFrame, str, bytes))


# =========================================================
# ✅ MFI
# =========================================================


@pytest.mark.integration
@pytest.mark.parametrize(
    "func,args,kwargs",
    [
        ("get_mfi_surveys", (), {}),
        ("get_mfi_surveys_full_data", (), {"survey_id": 123}),
        ("get_mfi_surveys_processed_data", (), {"survey_id": 123}),
        ("get_mfi_surveys_base_data", (), {"survey_id": 123}),
        ("get_mfi_xls_forms", (), {}),
        ("get_mfi_xls_forms_detailed", (), {"adm0_code": 231}),
        (
            "get_mfi_xls_forms_detailed",
            (),
            {
                "adm0_code": 231,
                "start_date": "2023-01-01",
                "end_date": "2023-12-31",
            },
        ),
    ],
)
def test_mfi_endpoints(client, func, args, kwargs):
    method = getattr(client, func)
    result = method(*args, **kwargs)
    assert isinstance(result, (pd.DataFrame, str, bytes))


# # =========================================================
# # ✅ FORBIDDEN ENDPOINTS
# # =========================================================

# @pytest.mark.integration
# @pytest.mark.parametrize(
#     "func,args,kwargs",
#     [
#         ("get_household_survey", (3094, "draft"), {}),
#         ("get_global_outlook", ("country_latest",), {}),
#         ("get_global_outlook", ("global_latest",), {}),
#         ("get_global_outlook", ("regional_latest",), {}),
#     ],
# )
# def test_forbidden_endpoints(client, func, args, kwargs):
#     result = method(*args, **kwargs)

#     if isinstance(result, pd.DataFrame):
#         assert result.empty or "403" in str(result)
#     else:
#         assert "403" in str(result)
