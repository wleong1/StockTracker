"""This module reads csv data files and processes them into the required format"""

from typing import Union
import os
import pandas as pd


class Model:
    """Processes data and returns data in required format"""

    def __init__(self) -> None:
        self.path: str = (
            "../individual_stocks_5yr/"
        )

    def generate_company_list(self) -> list:
        """
        Returns a list of companies.

        :return: (list) A list of companies.
        """
        company_list: list = []
        expected_headers: list = ["date", "close"]
        for _, _, filenames in os.walk(self.path):
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
        has_expected_headers: bool = False
        has_data: bool = False
        try:
            parse_dates: list = ["date"]
            df: pd.DataFrame = pd.read_csv(  # pylint: disable=C0103
                self.path + file,
                skip_blank_lines=True,
                dtype={"date": "string", "close": "float64"},
                parse_dates=parse_dates,
            )
            headers: set = set(df.columns.to_list())
            expected_headers_copy: list = expected_headers[:]
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
            df.iloc[[0]]  # pylint: disable=E1101,W0104
            has_data = True
        except (ValueError, IndexError, NameError):
            return False
        return has_expected_headers and has_data

    def process_data(self, expected_headers: list) -> Union[pd.DataFrame, str]:
        """
        Slices the data as required.

        :return: (DataFrame) A DataFrame containing required information of all companies.
        """
        companies_list: list = self.generate_company_list()
        companies_data: dict = {}
        try:
            for company in companies_list:
                csv_file: str = f"{self.path}{company}_data.csv"
                parse_dates: list = ["date"]
                df: pd.DataFrame = pd.read_csv(  # pylint: disable=C0103
                    csv_file,
                    header=0,
                    usecols=expected_headers,
                    skip_blank_lines=True,
                    dtype={"date": "string", "close": "float64"},
                    parse_dates=parse_dates,
                )
                df.dropna(how="all", subset="date", inplace=True)
                df.interpolate(method="linear", inplace=True)  # pylint: disable=E1101
                df["date"] = pd.to_datetime(df["date"])
                df["date"] = df["date"].dt.strftime("%Y-%m-%d")
                df["close"] = pd.to_numeric(df["close"])
                modified_data: dict = df.to_dict("list")
                companies_data[company] = modified_data
            all_companies_data: pd.DataFrame = pd.DataFrame(companies_data)
            return all_companies_data
        except (ValueError, TypeError, KeyError):
            return (
                "Please ensure each header is unique, data is correct, "
                "or expected_headers and process_data are configured correctly"
            )
