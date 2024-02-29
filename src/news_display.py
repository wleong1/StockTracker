from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel
from PyQt5.QtGui import QFont
import requests

from src.parameters import NEWS_API_KEY

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


class NewsDisplay:
    """Obtains and handles recent news"""

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    def collect_news(self, company_name: str) -> list:
        """
        Collect recent news articles related to a specific company and format them.

        :param company_name: (str) The name of the company to collect news for.
        :return: (list) A list of formatted news headlines with respective URLs.
        """
        news_params: dict = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": company_name
        }

        news_response: requests.models.Response = requests.get(NEWS_ENDPOINT, params=news_params)
        articles: list = news_response.json()["articles"]
        five_articles: list = articles[:5]
        return self.format_news_django(five_articles)
    
    def format_news_pyqt(self, articles):
        # Generate formatted headlines with clickable URLs
        return [
            f"{article['title']}: '<a href=\"{article['url']}\">'{article['url']}'</a>'"
            for article in articles
        ]
    
    def format_news_django(self, articles):
        return [{"title":article["title"], "url":article["url"]} for article in articles]

