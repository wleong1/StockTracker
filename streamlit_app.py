"""This module configures the streamlit web app."""
import json
import requests
import plotly.express as px # type: ignore[import-untyped] # pylint: disable=E0401
import pandas as pd
import streamlit as st # type: ignore[import-untyped] # pylint: disable=E0401


company_list_response: requests.Response = requests.get(
    "http://core-modules:5000/model/generate_company_list"
    )
company_list: list = company_list_response.json()
st.write("Hello, let's learn more about a company together!")
company = st.selectbox("Pick a company", [None] + company_list)
st.write("You selected:", company)

if company:
    payload: dict = {"company": company}
    update_response: requests.Response = requests.post(
        "http://core-modules:5000/update_data", json=payload
        )
    price: float = update_response.json()["price"]
    news: list = update_response.json()["news"]
    st.sidebar.write(f"{company}'s most recent price: {price}")

    news_container = st.sidebar.container()
    for article in news:
        news_container.markdown(f"- [{article['title']}]({article['url']})")

    chart_data: dict = json.loads(update_response.json()["graph"])
    date: dict
    close: dict
    date, close = chart_data["date"].values(), chart_data["close"].values()
    df = pd.DataFrame(close, date)

    fig = px.line(df)

    fig.update_layout(
        title=company,
        xaxis_title='Date',
        yaxis_title='Close',
        width=800,
        height=600
    )

    st.plotly_chart(fig)
