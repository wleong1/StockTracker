from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QLabel
from PyQt5.QtGui import QFont
import requests

from parameters import NEWS_API_KEY

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


class NewsDisplay(QWidget):
    """Obtains and handles recent news"""

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.vbox_news = QVBoxLayout()
        self.company_news_section = QGroupBox("Live news")
        self.company_news_section.setMaximumSize(700, 500)
        self.company_news_section.setFont(QFont("Times", 9))

    def display_company_news(self, company_name: str):
        """Displays news headlines for a given company name"""
        company_news = self.collect_news(company_name=company_name)

        # Remove news from previously selected company, if any
        while self.vbox_news.count():
            item = self.vbox_news.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Add news from currently selected company, if any
        for headline in company_news:
            news_label = QLabel(headline)
            news_label.setWordWrap(True)
            self.vbox_news.addWidget(news_label)

        self.company_news_section.setLayout(self.vbox_news)

    @staticmethod
    def collect_news(company_name: str):
        """Collects recent news articles for a given company name"""
        news_params = {
            "apiKey": NEWS_API_KEY,
            "qInTitle": company_name
        }

        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        articles = news_response.json()["articles"]
        five_articles = articles[:5]

        # Generate formatted headlines with clickable URLs
        return [
            f"{article['title']}: '<a href=\"{article['url']}\">'{article['url']}'</a>'"
            for article in five_articles
        ]
