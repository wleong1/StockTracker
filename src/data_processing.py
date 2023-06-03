import pandas as pd


class DataProcessing:
    """Accesses csv files directory and converts the csv files to dictionaries"""
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.path = "../individual_stocks_5yr/"

    def convert_to_dict(self, company_name: str) -> dict:
        """
        Converts csv files to pandas dataframe, and converts the dataframe to dictionary

        Args:
            company_name (str): Name of the company

        Returns:
            dict: Dictionary containing the converted data
        """
        csv_file_dir = f"{self.path}{company_name}_data.csv"
        df = pd.read_csv(csv_file_dir, header=0, usecols=["date", "open", "high", "low", "close"])
        modified_data = df.to_dict("list")
        return modified_data
