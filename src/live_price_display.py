"""This module returns the most recent price of the selected company."""

from typing import Union, Any
import requests
import yfinance as yf  # type: ignore[import-not-found] # type: ignore[import-untyped] # pylint: disable=E0401
import pandas as pd
import numpy as np
# import psycopg2

from parameters import ALPHA_VANTAGE_API_KEY  # type: ignore[attr-defined]

ALPHA_VANTAGE_ENDPOINT = "https://www.alphavantage.co/query"
JAVA_ENDPOINT = "http://172.18.34.111:8080"


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
            df: pd.DataFrame = pd.DataFrame(yf.download([company_name]))  # pylint: disable=C0103
            price: float = df.iloc[-1]["Close"]
            return round(price.values[0], 5)
        except IndexError:
            return "Error fetching price"
        
    @staticmethod
    def display_final_price_spring_boot(company_name: str) -> Union[float, str]:
        try:
            price_response: requests.models.Response = requests.get(
                f"{JAVA_ENDPOINT}/price/{company_name}" , timeout=20
            )
            return np.float64(price_response.json())
        except Exception as e:
            return e
        
# print(float(LivePriceDisplay().display_final_price_spring_boot("AAL")))
# print(type(LivePriceDisplay().display_final_price_yf("AAPL")))

# def get_price_from_java(company_name: str) -> Union[float, str]:
#     try:
#         # Call the Java microservice
#         response = requests.get(f"{JAVA_ENDPOINT}/price/{company_name}", timeout=20)
        
#         # Raise exception for HTTP errors
#         response.raise_for_status()
        
#         # Parse JSON safely
#         data = response.json()  # Expecting {"price": 123.45} or similar
        
#         # Extract price from JSON
#         price = np.float64(data["price"])
#         return price
#     except requests.exceptions.RequestException as e:
#         # Network, timeout, connection errors
#         print(f"Request failed: {e}")
#         return "N/A"
#     except (ValueError, KeyError, TypeError) as e:
#         # JSON parse errors or missing fields
#         print(f"Error parsing response from Java microservice: {e}")
#         return "N/A"