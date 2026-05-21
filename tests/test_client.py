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

pytest.mark.integration
@pytest.mark.parametrize(
    "func,args,kwargs",
    [
        # Prices
        ("get_prices", ("KEN",), {}),
        ("get_prices", ("KEN",), {"start_date": "2025-01-01", "end_date": "2025-12-31"}),

        # Exchange rates
        ("get_exchange_rates", ("ETH",), {}),

        # Food security
        ("get_food_security_list", ("ETH", 2025), {}),

        # Commodities
        ("get_commodities_list", (), {}),
        ("get_commodities_list", (), {"country_iso3": "TZA"}),
        ("get_commodities_list", (), {"commodity_name": "Maize"}),
        ("get_commodities_list", (), {"commodity_id": 123}),

        # Commodity units
        ("get_commodity_units_list", (), {"country_iso3": "TZA"}),
        ("get_commodity_units_list", (), {"commodity_unit_name": "Kg"}),
        ("get_commodity_units_list", (), {"commodity_unit_id": 5}),

        # Commodity unit conversions
        ("get_commodity_units_conversion_list", (), {}),
        ("get_commodity_units_conversion_list", (), {"country_iso3": "TZA"}),

        # Currency
        ("get_currency_list", (), {"country_iso3": "TZA"}),
        ("get_currency_list", (), {"currency_name": "ETB"}),
        ("get_currency_list", (), {"currency_id": 1}),

        # USD indirect quotation
        ("get_usd_indirect_quotation", (), {"country_iso3": "ETH"}),
        ("get_usd_indirect_quotation", (), {"currency_name": "ETB"}),

        # Economic indicators
        ("get_economic_indicator_list", (), {}),
        ("get_economic_indicator_list", (), {"indicator_name": "", "country_iso3": ""}),

        # Markets
        ("get_markets_list", ("AFG",), {}),
        ("get_markets_as_csv", ("AFG",), {}),
        ("get_markets_as_csv", ("AFG",), {"local_names": True}),
        ("get_nearby_markets", ("AFG", 34.515, 69.208), {}),
        ("get_market_geojson_list", ("AFG",), {}),

        # GORP
        ("get_gorp", ("country_latest",), {}),
        ("get_gorp", ("global_latest",), {}),
        ("get_gorp", ("regional_latest",), {}),

        # Household surveys
        ("get_household_survey", (3094, "official"), {}),
        ("get_household_survey", (3094, "public"), {}),
        ("get_household_surveys_list", (), {"country_iso3": "COG"}),
        ("get_household_surveys_list", (), {"country_iso3": "COG", "start_date": "2024-01-01", "end_date": "2024-12-31"}),

        # XLS forms
        ("get_household_xslform_definition", (2067,), {}),
        ("get_household_questionnaire", (2075,), {}),
        ("get_choice_list", (123,), {}),

        # MFI surveys
        ("get_mfi_surveys", (), {}),
        ("get_mfi_surveys_full_data", (), {"survey_id": 123}),
        ("get_mfi_surveys_processed_data", (), {"survey_id": 123}),
        ("get_mfi_surveys_base_data", (), {"survey_id": 123}),

        # MFI XLS forms
        ("get_mfi_xls_forms", (), {}),
        ("get_mfi_xls_forms_detailed", (), {"adm0_code": 231}),
        ("get_mfi_xls_forms_detailed", (), {"adm0_code": 231, "start_date": "2023-01-01", "end_date": "2023-12-31"}),
    ],
)

def test_endpoints_success(client, func, args, kwargs):
    method = getattr(client, func)

    result = method(*args, **kwargs)

    assert isinstance(result, (pd.DataFrame, str, bytes))

# # =========================================================
# # ✅ 4. FORBIDDEN ENDPOINT TESTS (expect 403)
# # =========================================================

pytest.mark.integration
@pytest.mark.parametrize(
    "func,args,kwargs",
    [ 
        # AIMS
        ("get_aims_analysis_rounds", (231,), {}),
        ("get_aims_polygon_files", (231,), {}),
        ("get_household_survey", (3094, "draft"), {}),
        # Add more endpoints known to require permissions
    ],
)
def test_endpoints_forbidden(client, func, args, kwargs):
    method = getattr(client, func)

    with pytest.raises(ApiException) as exc:
        method(*args, **kwargs)

    assert exc.value.status == 403
