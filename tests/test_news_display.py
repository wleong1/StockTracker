import pytest
from unittest.mock import patch
from src.news_display import NewsDisplay

@pytest.fixture
def test_news_display():
    yield NewsDisplay()

@patch("src.news_display.NewsDisplay._collect_news")
def test_collect_news(mock_get, test_news_display):
    mock_get.return_value = [
        {'title': 'Some headlines',
        'author': None,
        'source': {
        'id': None,
        'name': 'website name'
        },
        'publishedAt': 'timestamp',
        'url': 'url link'
        }
    ]
    results = test_news_display._collect_news()
    assert isinstance(results, list)
    assert ("title" in results[0] and results[0]["title"] is not None
            and "url" in results[0] and results[0]["url"] is not None)

@patch("src.news_display.NewsDisplay.format_news_pyqt")
def test_format_news_pyqt(mock_get, test_news_display):
    mock_get.return_value = [
            f"'title': '<a href=\"'url'\">''url''</a>'"
        ]
    results = test_news_display.format_news_pyqt()
    assert isinstance(results, list)
    assert "title" in results[0] and "href" in results[0]

@patch("src.news_display.NewsDisplay.format_news_django")
def test_format_news_django(mock_get, test_news_display):
    mock_get.return_value = [{"title":"title", "url":"url"}]
    results = test_news_display.format_news_django()
    assert isinstance(results, list)
    assert isinstance(results[0], dict)
    assert ("title" in results[0] and results[0]["title"] is not None
            and "url" in results[0] and results[0]["url"] is not None)