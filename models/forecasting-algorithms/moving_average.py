from parameters import mongodb_connection
from pymongo import MongoClient


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
        self.best_results = {"algo": None, "MSE": float("inf"), "window": None, "smoothing_factor": None}
    
    def simple_moving_average(self, window):
        dataset_length = len(self.dataset)
        total_squared_error = 0
        total_average_error = 0
        start, end = 0, window
        curr_sum = sum(self.dataset[:end])
        actual_data = self.dataset[end]
        curr_average_error = actual_data - curr_sum / window
        total_average_error += abs(curr_average_error)
        curr_squared_error = curr_average_error ** 2
        total_squared_error += curr_squared_error
        for end in range(window + 1, dataset_length):
            curr_sum = curr_sum + self.dataset[end - 1] - self.dataset[start]
            start += 1
            actual_data = self.dataset[end]
            curr_average_error = actual_data - curr_sum / window
            total_average_error += abs(curr_average_error)
            curr_squared_error = curr_average_error ** 2
            total_squared_error += curr_squared_error
        mean_absolute_error = total_average_error / (dataset_length - window)
        mean_squared_error = total_squared_error / (dataset_length - window)
        root_mean_squared_error = mean_squared_error ** 0.5
        self.sma_results[window] = {
            "mean_absolute_error": mean_absolute_error, 
            "mean_squared_error": mean_squared_error, 
            "root_mean_squared_error": root_mean_squared_error
            }
        if mean_squared_error < self.best_results["MSE"]:
            self.best_results["algo"] = "sma"
            self.best_results["MSE"] = mean_squared_error
            self.best_results["window"] = window
            self.best_results["smoothing_factor"] = None
        return (curr_sum + self.dataset[end] - self.dataset[start]) / window

    def exponential_moving_average(self, smoothing_factor):
        dataset_length = len(self.dataset)
        total_squared_error = 0
        total_error = 0
        # first_data = self.dataset[0]["close"]
        first_data = self.dataset[0]
        # second_data = self.dataset[1]["close"]
        second_data = self.dataset[1]
        curr_error = second_data - first_data
        total_error += abs(curr_error)
        curr_squared_error = curr_error ** 2
        # print(curr_error)
        total_squared_error += curr_squared_error
        for end in range(2, dataset_length):
            predicted_value = smoothing_factor * second_data + (1 - smoothing_factor) * first_data
            # print(f"predicted: {predicted_value}")
            # actual_data = self.dataset[end]["close"]
            actual_data = self.dataset[end]
            curr_error = actual_data - predicted_value
            total_error += abs(curr_error)
            curr_squared_error = curr_error ** 2
            # print(curr_error)
            total_squared_error += curr_squared_error
            first_data = predicted_value
            second_data = actual_data
        mean_absolute_error = total_error / (dataset_length - 1)
        mean_squared_error = total_squared_error / (dataset_length - 1)
        root_mean_squared_error = mean_squared_error ** 0.5
        self.ema_results[smoothing_factor] = {
            "mean_absolute_error": mean_absolute_error, 
            "mean_squared_error": mean_squared_error, 
            "root_mean_squared_error": root_mean_squared_error
            }
        if mean_squared_error < self.best_results["MSE"]:
            self.best_results["algo"] = "ema"
            self.best_results["MSE"] = mean_squared_error
            self.best_results["window"] = None
            self.best_results["smoothing_factor"] = smoothing_factor
        return smoothing_factor * second_data + (1 - smoothing_factor) * first_data

    def run_forecast(self):
        for window in self.window_size:
            predicted_value = self.simple_moving_average(window)
            self.sma_predictions.append(predicted_value)
        
        for smoothing_factor in self.smoothing_factor:
            predicted_value = self.exponential_moving_average(smoothing_factor)
            self.ema_predictions.append(predicted_value)

        return self.sma_results, self.sma_predictions, self.ema_results, self.ema_predictions
    
a = MovingAverage("AAPL")
a.run_forecast()
print(a.best_results)
