import json, argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm


class MonteCarloForecast:
        
    def __init__(self) -> None:
        with open("data.txt", "r") as file:
            raw_data = file.read()
        raw_data = raw_data.replace("'", "\"")
        data = json.loads(raw_data)
        self.processed_data = [{"date": data_point["date"], "close": float(data_point["close"])} for data_point in data]
        self.df = pd.DataFrame.from_dict(self.processed_data)

    def generate_mape(self, days_to_test, days_to_predict, number_of_simulations, return_mode):
        self.df.date = pd.to_datetime(mc.df.date)
        daily_return = np.log(1 + self.df.close.pct_change())
        average_daily_return = daily_return.mean()
        variance = daily_return.var()
        drift = average_daily_return - (variance/2)
        standard_deviation = daily_return.std()
        days_to_test = eval(days_to_test)
        days_to_predict = eval(days_to_predict)
        number_of_simulations = eval(number_of_simulations)
        predictions = np.zeros(days_to_test + days_to_predict)
        predictions[0] = self.df.close[days_to_test + days_to_predict]
        pred_collection = np.ndarray(shape=(number_of_simulations, days_to_test + days_to_predict))
        curr_mean_absolute_error = 0
        differences = np.array([])
        for sim_idx in range(0,number_of_simulations):
            for prediction_idx in range(1, days_to_test + days_to_predict):
                random_value = standard_deviation * norm.ppf(np.random.rand())
                predictions[prediction_idx] = predictions[prediction_idx - 1] * np.exp(drift + random_value)
            pred_collection[sim_idx] = predictions
            actual_values = self.df.close[:days_to_test]
            predicted_values = predictions[:days_to_test]
            curr_mean_absolute_error += np.mean(np.abs(predicted_values - actual_values) / np.abs(actual_values))
            if return_mode != "MAPE only":
                difference_array = np.subtract(predicted_values, actual_values)
                difference_value = np.sum(np.abs(difference_array))
                differences = np.append(differences, difference_value)

        if return_mode != "MAPE only":
            best_fit = np.argmin(differences)
            future_prices = pred_collection[best_fit][days_to_predict * -1:]
    

        Mean_Absolute_Percentage_Error = curr_mean_absolute_error / number_of_simulations * 100
        if return_mode == "forecast only":
            return future_prices 
        elif return_mode == "both":
            return Mean_Absolute_Percentage_Error, future_prices
        elif return_mode == "MAPE only":
            return Mean_Absolute_Percentage_Error
    

if __name__ == "__main__":
    mc = MonteCarloForecast()

    parser = argparse.ArgumentParser(description='Finding Mean Absolute Percentage Error using Monte Carlo Simulation')
    parser.add_argument('days_to_test', help='Provide the number of days to test')
    parser.add_argument('days_to_predict', help='Provide the number of days to predict')
    parser.add_argument('number_of_simulations', help='Provide the number of simulations to run')
    parser.add_argument('return_mode', help='Output to be returned, choose one of the modes: "forecast only", "both", or "MAPE only"')
    args = parser.parse_args()

    mc.generate_mape(args.days_to_test, args.days_to_predict, args.number_of_simulations, args.return_mode)
