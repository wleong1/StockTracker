from PyQt5.QtWidgets import QWidget, QLabel
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
import requests

from data_processing import DataProcessing
from parameters import ALPHA_VANTAGE_API_KEY

ALPHA_VANTAGE_ENDPOINT = "https://www.alphavantage.co/query"


class LivePriceDisplay(QWidget):
    """Shows the live prices"""

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.share_price_label = QLabel("Live price")
        self.share_price_label.setMaximumSize(700, 500)
        self.share_price_label.setFont(QFont("Times", 24))
        self.share_price_label.setAlignment(QtCore.Qt.AlignCenter)

    def display_final_price(self, company_name: str) -> None:
        """
        Fetches the live price of a company and updates the display label

        Args:
            company_name (str): Name of the company

        Returns:
            None

        """
        try:
            # Gets last available price by default
            price = DataProcessing().convert_to_dict(company_name=company_name)["close"][-1]

            price_params = {
                "apikey": ALPHA_VANTAGE_API_KEY,
                "function": "TIME_SERIES_DAILY_ADJUSTED",
                "symbol": company_name
            }

            price_response = requests.get(ALPHA_VANTAGE_ENDPOINT, params=price_params)
            if price_response.ok:
                response_data = price_response.json()
                if "Time Series (Daily)" in response_data:
                    price_list = response_data["Time Series (Daily)"]
                    most_recent_day = next(iter(price_list))
                    price = price_list[most_recent_day]["4. close"]

        except (requests.RequestException, KeyError, IndexError):
            price = "Error fetching price"

        self.share_price_label.setText(f"{company_name}:\n{price}")
