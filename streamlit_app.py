"""This module configures the streamlit web app."""

from typing import Union, Any
import json
import requests
import plotly.express as px # type: ignore[import-untyped] # pylint: disable=E0401
import pandas as pd
import streamlit as st # type: ignore[import-untyped] # pylint: disable=E0401
from model import Model
from live_price_display import LivePriceDisplay # type: ignore[import-untyped]
from news_display import NewsDisplay

models: Model = Model()
news_disp: NewsDisplay = NewsDisplay()
price_disp: LivePriceDisplay = LivePriceDisplay()
all_data: Union[pd.DataFrame, Any] = models.process_data()

company_list: list
company_list, _ = models.generate_company_list()
st.write("Hello, let's learn more about a company together!")
company = st.selectbox("Pick a company", [None] + company_list)
st.write("You selected:", company)

if company:
    price: float = price_disp.display_final_price_yf(company)
    news: list = news_disp.format_news_django(company)
    st.sidebar.write(f"{company}'s most recent price: {price}")

    news_container = st.sidebar.container()
    for article in news:
        news_container.markdown(f"- [{article['title']}]({article['url']})")

    raw_data: pd.Series = all_data[company]
    # data: dict = {
    #     "date": raw_data["trade_date"],
    #     "close": raw_data["close"]
    # }
    # df: pd.DataFrame = pd.DataFrame(data)
    # chart_data: dict = json.loads(update_response.json()["graph"])
    # date: dict
    # close: dict
    # date, close = chart_data["date"].values(), chart_data["close"].values()
    df = pd.DataFrame(raw_data["close"], raw_data["trade_date"])

    fig = px.line(df)

    fig.update_layout(
        title=company,
        xaxis_title='Date',
        yaxis_title='Close',
        width=800,
        height=600
    )

    st.plotly_chart(fig)
