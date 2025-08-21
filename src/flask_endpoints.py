"""This module creates the endpoints to be called by streamlit."""

from typing import Union, Any
from flask import Flask, jsonify, request # pylint: disable=E0401
import pandas as pd
import sys # pylint: disable=C0411
import os # pylint: disable=C0411
sys.path.append(os.getcwd())
from src.model import Model # pylint: disable=C0413
from src.live_price_display import LivePriceDisplay # type: ignore[import-untyped] # pylint: disable=C0413
from src.news_display import NewsDisplay # pylint: disable=C0413


models: Model = Model()
news_disp: NewsDisplay = NewsDisplay()
price_disp: LivePriceDisplay = LivePriceDisplay()


app = Flask(__name__)

def update_graph(company: str) -> str:
    """
    This method gets the data from the selected company.

    Args:
        company: The ticker symbol of the company

    Returns:
        chart_data: A DataFrame containing required information of all companies
    """
    try:
        # all_data: Union[pd.DataFrame, Any] = models.process_data(company)
        raw_data = models.process_data(company)
        data: dict = {
            "date": raw_data[0],
            "close": raw_data[1]
        }
        df: pd.DataFrame = pd.DataFrame(data) # pylint: disable=C0103
        return df.to_json()
    except Exception as e:
        print(f"Error generating graph for {company}: {e}")
        return "{}"

def update_price(company: str) -> Union[float, str]:
    """
    Returns the price of the selected company using core modules.

    Args:
        company_name: The ticker symbol of the company.

    Returns:
        The most recent price.
    """
    try:
        # price: Union[float, str] = price_disp.display_final_price_yf(company)
        price: Union[float, str] = price_disp.display_final_price_spring_boot(company)
        return price
    except Exception as e:
        print(f"Error getting price for {company}: {e}")
        return "N/A"

def update_news(company: str) -> list:
    """
    Get the formatted news.

    Args:
        company: The ticker symbol of the company

    Returns:
        news: The most recent five articles
    """
    try:
        # news: list = news_disp.format_news_django(company)
        news: list = news_disp.format_news_spring_boot(company)
        return news
    except Exception as e:
        print(f"Error getting news for {company}: {e}")
        return []

@app.route("/model/generate_company_list", methods=["GET"])
def generate_company_list():
    """
    Returns the list of companies.

    Args:
        None.

    Returns:
        ticker_list: The list of companies in json format.
    """
    ticker_list: list
    ticker_list, _ = models.generate_company_list()
    return jsonify(ticker_list)

@app.route("/update_data", methods=["GET", "POST"])
def update_data():
    """
    Returns the data of the selected company.

    Args:
        None.

    Returns:
        response: The data for the selected company in json.
    """
    response: dict = {}
    data: dict = request.get_json()
    company: str = data["company"]
    print(f"Received company: {company}")
    processed_price: Union[float, str] = update_price(company)
    processed_news: list = update_news(company)
    processed_chart_data: str = update_graph(company)

    response["price"] = processed_price
    response["news"] = processed_news
    response["graph"] = processed_chart_data
    return jsonify(response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
