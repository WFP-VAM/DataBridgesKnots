from datetime import date, timedelta
from unittest.mock import MagicMock, patch

import pytest

from data_bridges_knots.endpoints.marketPricesApi import (
    DEFAULT_DATE_RANGE_DAYS,
    RFC3339_DATE_FORMAT,
    MarketPricesApi,
)


class StubMarketPricesClient(MarketPricesApi):
    """MarketPricesApi host with authentication stubbed out for unit tests."""

    def __init__(self):
        self.config = {}
        self.env = "prod"

    def _setup_configuration_and_authentication(self, config):
        return MagicMock()


@pytest.fixture
def get_prices_call():
    """Patch the generated client and yield the mocked monthly-prices call."""
    with (
        patch(
            "data_bridges_knots.endpoints.marketPricesApi.data_bridges_client"
        ) as mock_client_module,
        patch("data_bridges_knots.endpoints.marketPricesApi.time.sleep"),
    ):
        api_instance = mock_client_module.MarketPricesApi.return_value
        response = MagicMock()
        response.items = []
        response.total_items = 0
        api_instance.market_prices_price_monthly_get.return_value = response
        yield api_instance.market_prices_price_monthly_get


@pytest.mark.parametrize(
    "dates",
    [
        {"start_date": "2025-01-01"},
        {"end_date": "2025-12-31"},
        {"start_date": "2025-01-01", "end_date": "2025-12-31"},
    ],
)
def test_latest_value_only_with_dates_raises(get_prices_call, dates):
    client = StubMarketPricesClient()

    with pytest.raises(ValueError, match="latest_value_only"):
        client.get_prices("KEN", latest_value_only=True, **dates)

    get_prices_call.assert_not_called()


def test_latest_value_only_without_dates_succeeds(get_prices_call):
    client = StubMarketPricesClient()

    df = client.get_prices("KEN", latest_value_only=True)

    get_prices_call.assert_called_once()
    assert get_prices_call.call_args.kwargs["latest_value_only"] is True
    assert df.empty


def test_default_start_date_is_range_of_default_days(get_prices_call):
    client = StubMarketPricesClient()

    client.get_prices("KEN")

    kwargs = get_prices_call.call_args.kwargs
    expected_start = (date.today() - timedelta(days=DEFAULT_DATE_RANGE_DAYS)).strftime(
        RFC3339_DATE_FORMAT
    )
    expected_end = date.today().strftime(RFC3339_DATE_FORMAT)
    assert kwargs["start_date"] == expected_start
    assert kwargs["end_date"] == expected_end
    assert kwargs["start_date"] != kwargs["end_date"]


def test_explicit_dates_are_formatted_rfc3339(get_prices_call):
    client = StubMarketPricesClient()

    client.get_prices("KEN", start_date="2025-01-01", end_date="2025-06-30")

    kwargs = get_prices_call.call_args.kwargs
    assert kwargs["start_date"] == "2025-01-01T00:00:00+01:00"
    assert kwargs["end_date"] == "2025-06-30T00:00:00+01:00"
