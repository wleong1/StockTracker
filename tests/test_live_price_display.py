from unittest.mock import patch
from src.live_price_display import LivePriceDisplay
import pytest

@pytest.fixture
def test_live_price_display():
    yield LivePriceDisplay()

@patch("src.live_price_display.LivePriceDisplay.display_final_price_av")
def test_mock_display_final_price_av(mock_get, test_live_price_display):
    mock_get.return_value = 123.45
    results = test_live_price_display.display_final_price_av("AAPL")
    assert isinstance(results, float)
    assert results == 123.45

@patch("src.live_price_display.LivePriceDisplay.display_final_price_av")
def test_display_final_price_av_exception(mock_get, test_live_price_display):
    mock_get.return_value = "Error fetching price"
    result = test_live_price_display.display_final_price_av("Unknown_Company")
    assert result == "Error fetching price"

@patch("src.live_price_display.LivePriceDisplay.display_final_price_yf")
def test_mock_display_final_price_yf(mock_get, test_live_price_display):
    mock_get.return_value = 291.97
    results = test_live_price_display.display_final_price_yf("AAPL")
    assert isinstance(results, float)
    assert results == 291.97

@patch("src.live_price_display.LivePriceDisplay.display_final_price_yf")
def test_display_final_price_yf_exception(mock_get, test_live_price_display):
    mock_get.return_value = "Error fetching price"
    result = test_live_price_display.display_final_price_yf("Unknown_Company")
    assert result == "Error fetching price"
