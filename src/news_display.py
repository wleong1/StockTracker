"""This module displays the most recent news of the selected company if available"""

import requests

from src.parameters import NEWS_API_KEY # type: ignore[import-untyped] # pylint: disable=E0401, E0611

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


class NewsDisplay:
    """
    Returns the most recent news of the selected company, if any.
    """

    @staticmethod
    def _collect_news(company_name: str) -> list:
        """
        Collect recent news articles related to the selected company and format them.
        Args:
            company_name: The ticker symbol of the company

        Returns:
            five_article: The most recent five articles
        """
        news_params: dict = {"apiKey": NEWS_API_KEY, "qInTitle": company_name}

        news_response: requests.models.Response = requests.get(
            NEWS_ENDPOINT, params=news_params,
            timeout=20
        )
        articles: list = news_response.json()["articles"]
        five_articles: list = articles[:5]
        return five_articles

    def format_news_pyqt(self, company_name: str) -> list:
        """
        Formats the collected news to suit different PyQt5 UI.
        Args:
            company_name: The ticker symbol of the company

        Returns:
            five_article: The most recent five articles
        """
        news: list = self._collect_news(company_name)
        return [
            f"{article['title']}: '<a href=\"{article['url']}\">'{article['url']}'</a>'"
            for article in news
        ]

    def format_news_django(self, company_name: str) -> list:
        """
        Formats the collected news to suit different django UI.
        Args:
            company_name: The ticker symbol of the company

        Returns:
            five_article: The most recent five articles
        """
        news: list = self._collect_news(company_name)
        return [{"title": article["title"], "url": article["url"]} for article in news]
