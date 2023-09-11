import pandas as pd
from model import Model


class DataProcessing:
    """Accesses csv files directory and converts the csv files to dictionaries"""

    def __init__(self, parent=None):
        super().__init__()
        self.data = None
        self.parent = parent
        self.path: str = "../individual_stocks_5yr/"
        self.companies_list = Model().company_list
        self.companies_data = self.process_data()

    def process_data(self):
        companies_data: dict = {}
        for company in self.companies_list:
            csv_file: str = f"{self.path}{company}_data.csv"
            df: pd.DataFrame = pd.read_csv(
                csv_file, header=0, usecols=["date", "close"]
            )
            modified_data: dict = df.to_dict("list")
            companies_data[company] = modified_data
        self.data = pd.DataFrame(companies_data)
        return self.data
