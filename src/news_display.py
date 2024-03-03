import requests

from src.parameters import NEWS_API_KEY

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


class NewsDisplay:
    """Obtains and handles recent news"""

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent

    def _collect_news(self, company_name: str) -> list:
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
        return five_articles
    
    def format_news_pyqt(self, company_name):
        # Generate formatted headlines with clickable URLs
        news = self._collect_news(company_name)
        return [
            f"{article['title']}: '<a href=\"{article['url']}\">'{article['url']}'</a>'"
            for article in news
        ]
    
    def format_news_django(self, company_name):
        news = self._collect_news(company_name)
        return [{"title":article["title"], "url":article["url"]} for article in news]
