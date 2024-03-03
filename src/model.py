# import csv
import os, sys
import pandas as pd
sys.path.append(os.getcwd())


class Model:
    """Processes data and returns data in required format"""
    def __init__(self, parent=None):
        super().__init__()
        self.company_list = None
        self.parent = parent
        self.path: str = "/home/wleong/Personal_project/StockTracker/individual_stocks_5yr/" # This is relative from where you run the script, not where this script is

    def generate_company_list(self) -> list:
        """
        Returns a list of companies.

        :return: (list) A list of companies.
        """
        company_list: list = []
        expected_headers = ["date", "close"]
        for (dirpath, dirnames, filenames) in os.walk(self.path):
            for file in filenames:
                if file.endswith(".csv"):
                    if self.check_headers_and_data(file, expected_headers):
                        company_name: str = file[:-9]
                        company_list.append(company_name)
        company_list.sort()
        return company_list

    def check_headers_and_data(self, file, expected_headers) -> bool:
        """
        Checks if each csv file has the expected headers and at least one data point for each header
        :param filename: (str) The name of the file being checked
        :param expected_headers: (list) The list of headers required
        :return: (bool) The results of the file
        """
        has_expected_headers = False
        has_data = False
        try:
            parse_dates = ["date"]
            df = pd.read_csv(self.path + file, skip_blank_lines=True,
                    dtype={"date": "string", "close": "float64"},
                    parse_dates=parse_dates)
            headers = set(df.columns.to_list())
            expected_headers_copy = expected_headers[:]
            # Two conditions the while loop should break:
            # 1. No more headers in expected_headers_copy (all are met)
            # 2. At least one header is not met
            while expected_headers_copy:
                if expected_headers_copy[0] in headers:
                    expected_headers_copy.pop(0)
                else:
                    break
            if not expected_headers_copy:
                has_expected_headers = True
            else:
                return False
        except pd.errors.EmptyDataError:
            return False
        try:
            df.iloc[[0]]
            has_data = True
        except (ValueError, IndexError, NameError):
            return False
        return has_expected_headers and has_data
    # no data (done)
    # data on top and headers at the bottom (treated same way as wrong headers)
    # only headers (done)
    # only data (done)
    # when is it time to use numpy or pandas to filter:
    # empty rows of data (solved using pandas dropna)
    # Nan data(solved, same as whole row empty, whole row will be removed)
    # one empty data (solved, same as whole row empty, whole row will be removed)
    # blank rows before headers and data, might need to remove before check headers and data? can be within this function (solved using skip_blank_lines from pandas)
    
    # string data in float or float data in string (not tested here, should be done in pandas read_csv, which I have mocked)
    # repeated headers in csv (should be checked in process_data) (done)
    # repeated headers in expected headers (should be checked in process_data)(done)
    # what happens if expected headers is empty(does it return whole dataframe?)(done, nothing)

    def process_data(self, expected_headers) -> pd.DataFrame:
        """
        Slices the data as required.

        :return: (DataFrame) A DataFrame containing required information of all companies.
        """
        companies_list = self.generate_company_list()
        companies_data: dict = {}
        try:
            for company in companies_list:
                csv_file: str = f"{self.path}{company}_data.csv"
                parse_dates = ["date"]
                df: pd.DataFrame = pd.read_csv(
                    csv_file, header=0, usecols=expected_headers, skip_blank_lines=True,
                    dtype={"date": "string", "close": "float64"},
                    parse_dates=parse_dates)
                df.dropna(how="all", subset="date", inplace=True)
                df.interpolate(method='linear', inplace=True)
                df["date"] = pd.to_datetime(df["date"])
                df["date"] = df["date"].dt.strftime("%Y-%m-%d")
                df["close"] = pd.to_numeric(df["close"])
                modified_data: dict = df.to_dict("list")
                companies_data[company] = modified_data
            all_companies_data = pd.DataFrame(companies_data)
            return all_companies_data
        except (ValueError, TypeError, KeyError):
            return "Please ensure each header is unique, data is correct, or expected_headers and process_data are configured correctly"
# a = Model()
# a.path = "tests/sample_data/"
# filename = "CompanyH_data.csv"
# expected_headers = ["date", "closing"]
# b = a.check_headers_and_data(filename, expected_headers)
# print(b)

# hard to make multiple csv files and push
# use pandas to read csv and save it as df?
# then don't need to make csv, can make pandas df for tests
# maybe only make csv for generate_company_list?
# df for check_headers_and_data?