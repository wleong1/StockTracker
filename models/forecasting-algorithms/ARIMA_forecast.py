import json, argparse
from statsmodels.tsa.arima.model import ARIMA
from collections import deque
import pmdarima as pm
import numpy as np
import pandas as pd

class ARIMAForecast:

    def __init__(self) -> None:
        with open("data.txt", "r") as file:
            raw_data = file.read()
        raw_data = raw_data.replace("'", "\"")
        data = json.loads(raw_data)
        self.processed_data = [{"date": data_point["date"], "close": float(data_point["close"])} for data_point in data]
        self.df = pd.DataFrame.from_dict(self.processed_data)
        

    def find_nearest_date(self, date_offset, start_date, direction):
        if direction == "backwards":
            req_date = pd.to_datetime(start_date) - pd.DateOffset(days = date_offset)
        elif direction == "forwards":
            req_date = pd.to_datetime(start_date) + pd.DateOffset(days = date_offset)

        queue = deque([req_date])
        visited_dates = set()
        last_available_date = self.processed_data[0]["date"]
        while queue:
            req_date = queue.popleft().strftime('%Y-%m-%d')
            if req_date in visited_dates:
                continue
            idx = self.df[self.df.date == req_date].index.values
            if idx.size > 0:
                if (direction == "forwards" and req_date >= start_date) or (direction == "backwards" and req_date < start_date):
                    break
            visited_dates.add(req_date)
            queue.append(pd.to_datetime(req_date) - pd.DateOffset(days = 1))
            if req_date < last_available_date:
                queue.append(pd.to_datetime(req_date) + pd.DateOffset(days = 1))

        return start_date, req_date, idx[0]
    
    def slice_data(self, start_date, **kwargs):
        final_idx = kwargs.get("final_idx", None)
        start_idx = self.df[self.df.date == start_date].index.values[0]
        if final_idx:
            if final_idx > start_idx:
                return self.df.iloc[start_idx:final_idx]
            else:
                return self.df.iloc[start_idx:final_idx:-1]
        else: return self.df.iloc[:start_idx]

    def window_slice_optimisation(self, start_date):
        best_results = {"AIC": float("inf"), "combination":{"p": 0, "d": 0, "q": 0}}
        date_offset = 180
        curr_start_date = start_date
        _, curr_end_date, curr_end_idx = self.find_nearest_date(3*365, curr_start_date, "forwards")
        _, _, curr_goal_idx = self.find_nearest_date(date_offset, curr_end_date, "forwards")
        curr_end_sliced_data = self.slice_data(curr_start_date, final_idx = curr_end_idx)
        curr_goal_sliced_data = self.slice_data(curr_end_date, final_idx = curr_goal_idx)
        
        for p in range(0,4):
            for d in range(0, 3):
                for q in range(0, 4):
                    arima_model_manual = ARIMA(curr_end_sliced_data.close, order=(p, d, q), enforce_invertibility=False, enforce_stationarity=False)
                    model_manual = arima_model_manual.fit(method_kwargs={"warn_convergence": False})
                    aic_value_manual = model_manual.aic

        if aic_value_manual < best_results["AIC"]:
            best_results["AIC"] = float(aic_value_manual)
            best_results["combination"]["p"] = p
            best_results["combination"]["d"] = d
            best_results["combination"]["q"] = q
        p_manual, d_manual, q_manual = list(best_results["combination"].values())
        arima_model_manual = ARIMA(curr_end_sliced_data.close, order=(p_manual, d_manual, q_manual), enforce_invertibility=False, enforce_stationarity=False)
        model_manual = arima_model_manual.fit(method_kwargs={"warn_convergence": False})
        try:
            forecast_length = len(curr_goal_sliced_data)
            forecasted_values_manual = pd.Series(model_manual.forecast(forecast_length), index=self.df.close[curr_end_idx:curr_goal_idx:-1].index)
            actual_values = self.df.close[curr_end_idx:curr_goal_idx:-1]
            Mean_Average_Percentage_Error_manual = np.mean(np.abs(forecasted_values_manual - actual_values)/np.abs(actual_values)) * 100

            model_auto = pm.auto_arima(curr_end_sliced_data.close, seasonal=True, m=12)
            (p_auto, d_auto, q_auto) = model_auto.get_params()["order"]
            arima_model_auto = ARIMA(curr_end_sliced_data.close, order=(p_auto, d_auto, q_auto), enforce_invertibility=False, enforce_stationarity=False)
            model_auto = arima_model_auto.fit(method_kwargs={"warn_convergence": False})
            forecast_length = len(curr_goal_sliced_data)
            forecasted_values_auto = pd.Series(model_auto.forecast(forecast_length), index=self.df.close[curr_end_idx:curr_goal_idx:-1].index)
            actual_values = self.df.close[curr_end_idx:curr_goal_idx:-1]
            Mean_Average_Percentage_Error_auto = np.mean(np.abs(forecasted_values_auto - actual_values)/np.abs(actual_values)) * 100

            return Mean_Average_Percentage_Error_manual, Mean_Average_Percentage_Error_auto     
        except ValueError as e:
            return None, None
    
    def train_test_optimisation(self, backwards_duration):
        best_results_trained_manual = {"AIC": float("inf"), "combination":{"p": 0, "d": 0, "q": 0}}
        _, first_data_date, _ = self.find_nearest_date(backwards_duration, self.processed_data[0]["date"], "backwards")
        sliced_data = self.slice_data(first_data_date)
        train_value_index = len(sliced_data) * 8 // 10
        for p in range(0,4):
            for d in range(0, 3):
                for q in range(0, 4):
                    arima_model_manual = ARIMA(sliced_data.close[:train_value_index], order=(p, d, q), enforce_invertibility=False, enforce_stationarity=False)
                    model_manual = arima_model_manual.fit(method_kwargs={"warn_convergence": False})
                    aic_value = model_manual.aic
                    if aic_value < best_results_trained_manual["AIC"]:
                        best_results_trained_manual["AIC"] = aic_value
                        best_results_trained_manual["combination"]["p"] = p
                        best_results_trained_manual["combination"]["d"] = d
                        best_results_trained_manual["combination"]["q"] = q

        p_manual, d_manual, q_manual = list(best_results_trained_manual["combination"].values())
        arima_model_manual = ARIMA(sliced_data.close[:train_value_index], order=(p_manual, d_manual, q_manual), enforce_invertibility=False, enforce_stationarity=False)
        model_manual = arima_model_manual.fit(method_kwargs={"warn_convergence": False})               
        forecasted_values_manual = pd.Series(model_manual.forecast(len(sliced_data) - train_value_index),
                                    index=sliced_data.close[train_value_index:].index)
        actual_values = sliced_data.close[train_value_index:]

        Mean_Average_Percentage_Error_manual = np.mean(np.abs(forecasted_values_manual - actual_values)/np.abs(actual_values)) * 100

        model_auto = pm.auto_arima(sliced_data.close, seasonal=True, m=12)
        (p_auto, d_auto, q_auto) = model_auto.get_params()["order"]
        arima_model_auto = ARIMA(sliced_data.close[:train_value_index], order=(p_auto, d_auto, q_auto), enforce_invertibility=False, enforce_stationarity=False)
        model_auto = arima_model_auto.fit(method_kwargs={"warn_convergence": False})
        forecasted_values_auto = pd.Series(model_auto.forecast(len(sliced_data) - train_value_index),
                                    index=sliced_data.close[train_value_index:].index)
        actual_values = self.df.close[train_value_index:]
        Mean_Average_Percentage_Error_auto = np.mean(np.abs(forecasted_values_auto - actual_values)/np.abs(actual_values)) * 100

        return Mean_Average_Percentage_Error_manual, Mean_Average_Percentage_Error_auto
    
    def generate_mape(self, start_date, slice_window, prediction_length, backwards_duration):
        dates = []
        dates.append(start_date)
        slice_final_date = self.find_nearest_date(slice_window, start_date, "forwards")[1]
        slice_window_manual_mape_list, slice_window_auto_mape_list = [], []
        manual_result, auto_result = self.window_slice_optimisation(dates[-1])
        slice_window_manual_mape_list.append(manual_result)
        slice_window_auto_mape_list.append(auto_result)
        while slice_final_date < self.processed_data[0]["date"]:
            start_date = self.find_nearest_date(prediction_length, dates[-1], "forwards")[1]
            dates.append(start_date)
            manual_result, auto_result = self.window_slice_optimisation(dates[-1])
            if manual_result and auto_result:
                slice_window_manual_mape_list.append(manual_result)
                slice_window_auto_mape_list.append(auto_result)
            slice_final_date = self.find_nearest_date(slice_window, start_date, "forwards")[1]
        
        if slice_window_manual_mape_list[0] != None and slice_window_auto_mape_list[0] != None:
            manual_series = pd.Series(slice_window_manual_mape_list)
            auto_series = pd.Series(slice_window_auto_mape_list)
            mape_manual = np.mean(manual_series)
            mape_auto = np.mean(auto_series)
        else: 
            print("Not enough data provided, please provide more data, or reduce the slice window or prediction length")
        
        try:
            train_test_manual_mape, train_test_auto_mape = self.train_test_optimisation(backwards_duration)        
        except ValueError as e:
            print("Data too short to split")
            train_test_manual_mape, train_test_auto_mape = None, None
        except IndexError as e:
            print("Need more data points")
            train_test_manual_mape, train_test_auto_mape = None, None


        return(f"""Results:\n
                sliced window manual mape: {mape_manual},\n 
                sliced window auto mape: {mape_auto},\n
                train test manual mape: {train_test_manual_mape},\n
                train test auto mape: {train_test_auto_mape}""")

if __name__ == "__main__":
    af = ARIMAForecast()

    parser = argparse.ArgumentParser(description='Finding Mean Absolute Percentage Error using two different methods')
    parser.add_argument('start_date', help='Provide date to start the slice, ensure date has data')
    parser.add_argument('slice_window', help='The window size of the slice used for analysis')
    parser.add_argument('prediction_length', help='The number of data points to be predicted')
    parser.add_argument('backwards_duration', help='How far back would the first data be, in days')
    args = parser.parse_args()

    af.generate_mape(args.start_date, args.slice_window, args.prediction_length, args.backwards_duration)
