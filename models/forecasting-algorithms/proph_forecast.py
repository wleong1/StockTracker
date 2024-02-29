import pandas as pd
from prophet import Prophet
from parameters import mongodb_connection
from pymongo import MongoClient
import numpy as np
import argparse

class ProphForecast:

    def __init__(self) -> None:
        client = MongoClient(mongodb_connection)
        database = client.StockTracker
        collection = database.Companies
        projection = {"_id": 1, "price": 1}
        cursor = collection.find({"_id": "AAPL"}, projection)
        for doc in cursor:
            self.all_points = doc["price"]

    def generate_mape(self, days_to_test, days_to_predict):
        days_to_test = eval(days_to_test)
        days_to_predict = eval(days_to_predict)
        df = pd.DataFrame.from_dict(self.all_points[:days_to_test][::-1])
        new_headers = {"date": "ds",
                       "close": "y"}
        df.rename(columns=new_headers,
                  inplace=True)
        m = Prophet()
        m.fit(df)
        future = m.make_future_dataframe(periods=days_to_predict)
        forecast = m.predict(future)
        actual_prices = pd.Series([float(price) for price in df["y"].values.tolist()])
        forecasted_prices = pd.Series([price[0] for price in forecast[["yhat"]].values.tolist()[:-1]])
        Mean_Absolute_Percentage_Error = np.mean(np.abs(forecasted_prices - actual_prices)/np.abs(actual_prices)) * 100
        return Mean_Absolute_Percentage_Error


if __name__ == "__main__":
    pf = ProphForecast()

    parser = argparse.ArgumentParser(description='Finding Mean Absolute Percentage Error using Prophet Forecast')
    parser.add_argument('days_to_test', help='Provide the number of days to test')
    parser.add_argument('days_to_predict', help='Provide the number of days to predict')
    args = parser.parse_args()

    pf.generate_mape(args.days_to_test, args.days_to_predict)
