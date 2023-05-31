import requests

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "ba1ce03bb02f432ca6f88efb7b475a47"


class NewsCollector:
    """Obtain news from newsapi.com"""

    @staticmethod
    def collect_news(company):
        news_params = {
            "apiKey": NEWS_API_KEY,
            "qInTitle": company
        }

        news_response = requests.get(NEWS_ENDPOINT, params=news_params)
        articles = news_response.json()["articles"]

        five_articles = articles[:5]
        return [f"{article['title']}" for article in five_articles] #TODO:PROVIDE URL
