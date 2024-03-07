"""This module returns the most recent price of the selected company."""

from typing import Union, Any
import requests
import yfinance as yf  # type: ignore[import-not-found] # type: ignore[import-untyped] # pylint: disable=E0401
import pandas as pd

from src.parameters import ALPHA_VANTAGE_API_KEY  # type: ignore[import-not-found] # pylint: disable=E0401, E0611

ALPHA_VANTAGE_ENDPOINT = "https://www.alphavantage.co/query"


class LivePriceDisplay:
    """
    Returns the most recent price of the selected company.
    """

    @staticmethod
    def display_final_price_av(company_name: str) -> Union[str, dict, Any]:
        """
        Returns a the price using Alpha Vantage.

        Args:
            company_name: The ticker symbol of the company

        Returns:
            The most recent price in string
        """
        try:
            # Gets last available price by default
            price_params: dict = {
                "apikey": ALPHA_VANTAGE_API_KEY,
                "function": "TIME_SERIES_DAILY",
                "symbol": company_name,
            }
            price_response: requests.models.Response = requests.get(
                ALPHA_VANTAGE_ENDPOINT, params=price_params, timeout=20
            )
            if price_response.ok:
                response_data: dict = price_response.json()
                if "Time Series (Daily)" in response_data:
                    price_list: dict = response_data["Time Series (Daily)"]
                    most_recent_day: str = next(iter(price_list))
                    return price_list[most_recent_day]["4. close"]
                return response_data
            return price_response

        except (
            requests.exceptions.MissingSchema,
            requests.RequestException,
            KeyError,
            IndexError,
        ):
            return "Error fetching price"

    @staticmethod
    def display_final_price_yf(company_name: str) -> Union[float, str]:
        """
        Returns a the price using Yahoo Finance.

        Args:
            company_name: The ticker symbol of the company

        Returns:
            The most recent price in string
        """
        try:
            df: pd.DataFrame = yf.download(company_name)  # pylint: disable=C0103
            price: float = df.iloc[-1]["Close"]
            return round(price, 5)
        except IndexError:
            return "Error fetching price"


# from pymongo import MongoClient
# client = MongoClient(mongodb_connection)
# database = client.StockTracker
# collection = database.Companies
# projection = {"_id": 0, "name": 1, "price": 1}
# cursor = collection.find({"name": "MSFT"}, projection)
# for doc in cursor:
#     latest_date = doc["price"][0]["date"]
# print(latest_date)
# symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "NVDA"]# "TSLA", "GOOG", "BRK.B", "META", "UNH"
# for symbol in symbols:
#     price_params: dict = {
#         "apikey": ALPHA_VANTAGE_API_KEY,
#         "function": "TIME_SERIES_DAILY",
#         "symbol": symbol,
#         "outputsize": "full"
#     }
#     a = requests.get(ALPHA_VANTAGE_ENDPOINT, params=price_params).json()
#     company = {"_id": symbol, "price":[{"date": b, "close": a["Time Series (Daily)"][b]["4. close"]} for b in a["Time Series (Daily)"]]} # pylint: disable=C0301
#     result = collection.insert_one(company)
#     print(f"Inserted document ID: {result.inserted_id}")
