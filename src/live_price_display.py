from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import requests

<<<<<<< HEAD
from data_processing import DataProcessing
from parameters import ALPHA_VANTAGE_API_KEY
=======
from processing.data_processing import DataProcessing
from parameters import ALPHA_VANTAGE_API_KEY, mongodb_connection
>>>>>>> a55d65f (Removed parameters)

ALPHA_VANTAGE_ENDPOINT = "https://www.alphavantage.co/query"


class LivePriceDisplay(QWidget):
    """Shows the live prices"""

    def __init__(self, parent=None):
        super().__init__()
        self.price = None
        self.parent = parent
        self.share_price_label = QLabel("Live price")
        self.share_price_label.setMaximumSize(700, 500)
        self.share_price_label.setFont(QFont("Times", 24))
        self.share_price_label.setAlignment(QtCore.Qt.AlignCenter)

    def display_final_price(self, company_name: str) -> None:
        """
        Attempts to display the final price of the selected company.

        :param company_name: (str) The name of the name to display the final price for.
        :return:
        """

        try:
            # Gets last available price by default
            price_params: dict = {
                "apikey": ALPHA_VANTAGE_API_KEY,
                "function": "TIME_SERIES_DAILY",
                "symbol": company_name
            }
            price_response: requests.models.Response = requests.get(ALPHA_VANTAGE_ENDPOINT, params=price_params)
            if price_response.ok:
                response_data: dict = price_response.json()
                if "Time Series (Daily)" in response_data:
                    price_list: dict = response_data["Time Series (Daily)"]
                    most_recent_day: str = next(iter(price_list))
                    self.price: float = price_list[most_recent_day]["4. close"]

        except (requests.RequestException, KeyError, IndexError):
            self.price: str = "Error fetching price"

        self.share_price_label.setText(f"{company_name}:\n{self.price}")

from pymongo import MongoClient
client = MongoClient(mongodb_connection)
database = client.StockTracker
collection = database.Companies
projection = {"_id": 0, "name": 1, "price": 1}
# cursor = collection.find({"name": "MSFT"}, projection)
# for doc in cursor:
#     latest_date = doc["price"][0]["date"]
# print(latest_date)
symbols = ["AAPL", "MSFT", "AMZN", "GOOGL", "NVDA"]# "TSLA", "GOOG", "BRK.B", "META", "UNH"
for symbol in symbols:
    price_params: dict = {
        "apikey": ALPHA_VANTAGE_API_KEY,
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": "full"
    }
    a = requests.get(ALPHA_VANTAGE_ENDPOINT, params=price_params).json()
    company = {"_id": symbol, "price":[{"date": b, "close": a["Time Series (Daily)"][b]["4. close"]} for b in a["Time Series (Daily)"]]}
    result = collection.insert_one(company)
    print(f"Inserted document ID: {result.inserted_id}")
