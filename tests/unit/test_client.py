import pytest
from dotenv import load_dotenv

from data_bridges_knots.client import (
    DataBridgesKnots,
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


# -------------------------
# ✅ 1. Import
# -------------------------


def test_deprecated_import():
    from data_bridges_knots.client import DataBridgesKnots

    assert DataBridgesKnots is not None


def test_import():
    from data_bridges_knots.client import DataBridgesKnots

    assert DataBridgesKnots is not None


# -------------------------
# ✅ 2. Config
# -------------------------


def test_deprecated_client_init(valid_config):
    client = DataBridgesKnots(valid_config)
    assert isinstance(client, DataBridgesKnots)


def test_client_init(valid_config):
    client = DataBridgesKnots(valid_config)
    assert isinstance(client, DataBridgesKnots)


# % HERE NEW TESTS


# # ======================================================
# # Fixtures
# # ======================================================

# @pytest.fixture
# def mock_item():
#     item = MagicMock()
#     item.to_dict.return_value = {"col": "value"}
#     return item


# @pytest.fixture
# def mock_api_response(mock_item):
#     response = MagicMock()
#     response.items = [mock_item]
#     response.total_items = 1
#     return response


# # ======================================================
# # config_from_env
# # ======================================================


# # def test_config_from_env_missing(monkeypatch):
# #     monkeypatch.delenv("WFP_API_CLIENT_ID", raising=False)

# #     with pytest.raises(ValueError):
# #         config_from_env()


# # ======================================================
# # Initialization
# # ======================================================

# def test_init_success(valid_config):
#     client = DataBridgesKnots(valid_config)
#     assert client.config == valid_config


# def test_validate_config_failure():
#     with pytest.raises(ValueError):
#         DataBridgesKnots({"WFP_API_CLIENT_ID": "only"})


# def test_load_config_dict(valid_config):
#     client = DataBridgesKnots(valid_config)
#     loaded = client._load_config(valid_config)
#     assert loaded == valid_config


# def test_load_config_type_error(valid_config):
#     client = DataBridgesKnots(valid_config)

#     with pytest.raises(TypeError):
#         client._load_config(123)


# # ======================================================
# # API MOCKING HELPERS
# # ======================================================

# def setup_mock_context(mock_client):
#     mock_client.return_value.__enter__.return_value = MagicMock()


# # ======================================================
# # get_prices
# # ======================================================

# @patch("data_bridges_knots.client.data_bridges_client.ApiClient")
# def test_get_prices(mock_api, mock_client, valid_config, mock_api_response):
#     setup_mock_context(mock_client)
#     mock_api.return_value.market_prices_price_monthly_get.return_value = mock_api_response

#     client = DataBridgesKnots(valid_config)

#     df = client.get_prices("KEN", start_date="2024-01-01")

#     assert isinstance(df, pd.DataFrame)
#     assert not df.empty


# # ======================================================
# # get_exchange_rates
# # ======================================================

# @patch("data_bridges_knots.client.data_bridges_client.ApiClient")
# @patch("data_bridges_knots.client.data_bridges_client.CurrencyApi")
# def test_get_exchange_rates(mock_api, mock_client, valid_config, mock_api_response):
#     setup_mock_context(mock_client)
#     mock_api.return_value.currency_usd_indirect_quotation_get.return_value = mock_api_response

#     client = DataBridgesKnots(valid_config)

#     df = client.get_exchange_rates("KEN")

#     assert len(df) == 1


# # ======================================================
# # get_commodities_list
# # ======================================================

# @patch("data_bridges_knots.client.data_bridges_client.ApiClient")
# @patch("data_bridges_knots.client.data_bridges_client.CommoditiesApi")
# def test_get_commodities_list(mock_api, mock_client, valid_config, mock_api_response):
#     setup_mock_context(mock_client)
#     mock_api.return_value.commodities_list_get.return_value = mock_api_response

#     client = DataBridgesKnots(valid_config)

#     df = client.get_commodities_list()

#     assert "col" in df.columns


# # ======================================================
# # get_market_geojson_list
# # ======================================================

# @patch("data_bridges_knots.client.get_adm0_code", return_value=123)
# @patch("data_bridges_knots.client.data_bridges_client.ApiClient")
# @patch("data_bridges_knots.client.data_bridges_client.MarketsApi")
# def test_get_market_geojson(mock_api, mock_client, mock_adm0, valid_config):
#     setup_mock_context(mock_client)

#     mock_response = MagicMock()
#     mock_response.model_dump.return_value = {"type": "FeatureCollection"}
#     mock_api.return_value.markets_geo_json_list_get.return_value = mock_response

#     client = DataBridgesKnots(valid_config)

#     result = client.get_market_geojson_list("KEN")

#     assert result["type"] == "FeatureCollection"


# def test_get_market_geojson_requires_param(valid_config):
#     client = DataBridgesKnots(valid_config)

#     with pytest.raises(ValueError):
#         client.get_market_geojson_list()


# # ======================================================
# # get_global_outlook
# # ======================================================

# @patch("data_bridges_knots.client.data_bridges_client.ApiClient")
# @patch("data_bridges_knots.client.data_bridges_client.GlobalOutlookApi")
# def test_get_global_outlook_country(mock_api, mock_client, valid_config, mock_api_response):
#     setup_mock_context(mock_client)
#     mock_api.return_value.global_outlook_country_latest_get.return_value = mock_api_response

#     client = DataBridgesKnots(valid_config)

#     df = client.get_global_outlook("country_latest")

#     assert isinstance(df, pd.DataFrame)


# def test_get_global_outlook_invalid(valid_config):
#     client = DataBridgesKnots(valid_config)

#     with pytest.raises(ValueError):
#         client.get_global_outlook("invalid")


# # ======================================================
# # Household questionnaire + choices
# # ======================================================

# def test_get_choice_list(valid_config):
#     client = DataBridgesKnots(valid_config)

#     client.xlsform = pd.DataFrame([{
#         "fields": [
#             {
#                 "choiceList": [
#                     {
#                         "name": "food",
#                         "choices": [
#                             {"name": "rice", "label": "Rice"}
#                         ]
#                     }
#                 ]
#             }
#         ]
#     }])

#     df = client.get_choice_list(1)

#     assert "value" in df.columns
#     assert "label" in df.columns


# # ======================================================
# # Error propagation
# # ======================================================

# @patch("data_bridges_knots.client.data_bridges_client.ApiClient")
# @patch("data_bridges_knots.client.data_bridges_client.MarketPricesApi")
# def test_get_prices_raises_api_exception(mock_api, mock_client, valid_config):
#     from data_bridges_knots.client import ApiException

#     setup_mock_context(mock_client)
#     mock_api.return_value.market_prices_price_monthly_get.side_effect = ApiException("fail")

#     client = DataBridgesKnots(valid_config)

#     with pytest.raises(ApiException):
#         client.get_prices("KEN")


# # ======================================================
# # String methods
# # ======================================================

# def test_repr(valid_config):
#     client = DataBridgesKnots(valid_config)
#     assert "DataBridgesKnots" in repr(client)


# def test_str(valid_config):
#     client = DataBridgesKnots(valid_config)
#     assert "API Host" in str(client)
