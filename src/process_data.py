import pandas as pd

class read_data_from_csv:
    """Gets required data from existing csv files"""
    def __init__(self, filename: str):
# TODO: Check if the filename actually exists
        self.filename = filename
        self.modes = ["open", "close", "high", "low"]

    def get_info(self, mode: str):
        if mode in self.modes:
            columns = ["date", mode]
            df = pd.read_csv(f"{self.filename}_data.csv", usecols=columns)
        else:
            print(f"Invalid mode: {mode}")
