"""This module returns the most recent price of the selected company."""

from typing import Union, Any
import requests
import yfinance as yf  # type: ignore[import-not-found] # type: ignore[import-untyped] # pylint: disable=E0401
import pandas as pd
# import psycopg2

from src.parameters import ALPHA_VANTAGE_API_KEY  # type: ignore[attr-defined]

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
            company_name: The ticker symbol of the company.

        Returns:
            The most recent price.
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
        Returns the price of the selected company using Yahoo Finance.

        Args:
            company_name: The ticker symbol of the company.

        Returns:
            The most recent price.
        """
        # Uncomment below for full company names in selection rather than ticker symbols.
        # conn = psycopg2.connect(database = "stocks", user='postgres', password='123456')
        # cursor = conn.cursor()
        # company_name = company_name.replace("\xa0", " ")
        # cursor.execute(f"SELECT ticker FROM companies WHERE company_name = '{company_name}';")
        # company_name = cursor.fetchall()[0]
        # conn.close()
        try:
            df: pd.DataFrame = yf.download(company_name)  # pylint: disable=C0103
            price: float = df.iloc[-1]["Close"]
            return round(price, 5)
        except IndexError:
            return "Error fetching price"
