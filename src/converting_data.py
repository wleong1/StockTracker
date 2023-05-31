import pandas as pd
from process_data import read_data_from_csv


class ConvertCsvToDict:
    """Converts the csv files to dictionaries for selected columns"""
    def __init__(self):
        self.path = "../individual_stocks_5yr/"

    def convert_to_dict(self, filename):
        csv_file_dir = f"{self.path}{filename}_data.csv"
        df = pd.read_csv(csv_file_dir, header=0, usecols=["date", "open", "high", "low", "close"])
        modified_data = df.to_dict("list")
        return modified_data

    # DELETE WHEN LIVE DATA API HAS BEEN OBTAINED #TODO:GET LIVE PRICES
    # Placeholder for live data
    def display_live_data(self, filename):
        data = self.convert_to_dict(filename=filename)["close"][-1]
        return data
