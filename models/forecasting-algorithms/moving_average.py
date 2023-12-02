from parameters import mongodb_connection
from pymongo import MongoClient
import pandas as pd
import numpy as np
import argparse


class MovingAverage:

    def __init__(self, company) -> None:
        client = MongoClient(mongodb_connection)
        database = client.StockTracker
        collection = database.Companies
        projection = {"_id": 1, "price": 1}
        cursor = collection.find({"_id": company}, projection)
        for doc in cursor:
            all_points = doc["price"]
        self.dataset = [float(closing_price["close"]) for closing_price in all_points]
        self.window_size = [window for window in range(10, 1000)]
        self.smoothing_factor = [smoothing_factor / 10 for smoothing_factor in range(1, 10)]
        self.sma_results = {}
        self.sma_predictions = []
        self.ema_results = {}
        self.ema_predictions = []
        self.best_results = {"algo": None, "MAPE": float("inf"), "window": None, "smoothing_factor": None}
        self.mape = float("inf")

    def simple_moving_average(self, window):
        dataset_length = len(self.dataset)
        start, end = 0, window
        curr_sum = sum(self.dataset[:end])
        actual_dataset, forecasted_dataset = [], []
        actual_data = self.dataset[end]
        actual_dataset.append(actual_data)
        forecasted_data = curr_sum / window
        forecasted_dataset.append(forecasted_data)
        # total_percentage_error = (abs(forecasted_data - actual_data) / actual_data) * 100
        for end in range(window + 1, dataset_length):
            curr_sum = curr_sum + self.dataset[end - 1] - self.dataset[start]
            start += 1
            actual_data = self.dataset[end]
            actual_dataset.append(actual_data)
            forecasted_data = curr_sum / window
            forecasted_dataset.append(forecasted_data)
            # total_percentage_error += (abs(forecasted_data - actual_data) / actual_data) * 100
        number_of_forecasts = dataset_length - window
        # MAPE = total_percentage_error / number_of_forecasts
        actual_dataset = pd.Series(actual_dataset)
        forecasted_dataset = pd.Series(forecasted_dataset)
        curr_mape = np.mean(np.abs(forecasted_dataset - actual_dataset)/np.abs(actual_dataset)) * 100
        self.sma_results[window] = {
            "MAPE": curr_mape
            # "MAPE": MAPE
            }

        # if self.mape < self.best_results["MAPE"]:
        if curr_mape < self.best_results["MAPE"]:
            self.best_results["algo"] = "sma"
            # self.best_results["MAPE"] = MAPE
            self.best_results["MAPE"] = curr_mape
            self.best_results["window"] = window
            self.best_results["smoothing_factor"] = None
        return (curr_sum + self.dataset[end] - self.dataset[start]) / window

    def exponential_moving_average(self, smoothing_factor):
        dataset_length = len(self.dataset)
        total_percentage_error = 0
        first_data = self.dataset[0]
        second_data = self.dataset[1]
        actual_dataset, forecasted_dataset = [], []
        actual_dataset.append(second_data)
        forecasted_dataset.append(first_data)
        curr_error = second_data - first_data
        total_percentage_error += (abs(curr_error) / second_data) * 100
        for end in range(2, dataset_length):
            forecasted_value = smoothing_factor * second_data + (1 - smoothing_factor) * first_data
            actual_data = self.dataset[end]
            actual_dataset.append(actual_data)
            forecasted_dataset.append(forecasted_value)
            curr_error = forecasted_value - actual_data
            total_percentage_error += (abs(curr_error) / actual_data) * 100
            first_data = forecasted_value
            second_data = actual_data
        actual_dataset = pd.Series(actual_dataset)
        forecasted_dataset = pd.Series(forecasted_dataset)
        curr_mape = np.mean(np.abs(forecasted_dataset - actual_dataset)/np.abs(actual_dataset)) * 100
        # MAPE = total_percentage_error / (dataset_length - 1)
        self.ema_results[smoothing_factor] = {
            # "MAPE": MAPE
            "MAPE": curr_mape
            }
        # if MAPE < self.best_results["MAPE"]:
        if curr_mape < self.best_results["MAPE"]:
            self.best_results["algo"] = "ema"
            # self.best_results["MAPE"] = MAPE
            self.best_results["MAPE"] = curr_mape
            self.best_results["window"] = None
            self.best_results["smoothing_factor"] = smoothing_factor
        return smoothing_factor * second_data + (1 - smoothing_factor) * first_data

    def run_forecast(self):
        for window in self.window_size:
            forecasted_value = self.simple_moving_average(window)
            self.sma_predictions.append(forecasted_value)
        
        for smoothing_factor in self.smoothing_factor:
            forecasted_value = self.exponential_moving_average(smoothing_factor)
            self.ema_predictions.append(forecasted_value)

        return self.sma_results, self.sma_predictions, self.ema_results, self.ema_predictions
    
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Finding Mean Absolute Percentage Error using two different moving averages')
    parser.add_argument('company_name', help='Provide company name to analyse')
    args = parser.parse_args()
    ma = MovingAverage(args.company_name)
    ma.run_forecast()
