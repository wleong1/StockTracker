"""This module reads csv data files and processes them into the required format"""

from typing import Union, Tuple
import warnings
import psycopg2  # pylint: disable=E0401
import pandas as pd

warnings.filterwarnings("ignore")


class Model:
    """Processes data and returns data in required format"""

    def __init__(self) -> None:
        self.path: str = "../individual_stocks_5yr/"

    @staticmethod
    def generate_company_list() -> Tuple[list, list]:
        """
        Returns a list of companies.

        :return: (list) A list of companies.
        """
        conn = psycopg2.connect(
            host="stocks-postgres",
            database="stocks",
            user="postgres",
            password="123456",
            port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM companies;")
        records = cursor.fetchall()
        ticker_list: list = []
        companies_list: list = []
        for row in records:
            (_, ticker, company) = row
            company = company.replace("\xa0", " ")
            ticker_list.append(ticker)
            companies_list.append(company)
        conn.close()
        return ticker_list, companies_list

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

    def process_data(self) -> Union[pd.DataFrame, str]:
        """
        Slices the data as required.

        :return: (DataFrame) A DataFrame containing required information of all companies.
        """
        companies_list: Tuple[list, list] = self.generate_company_list()
        companies_data: dict = {}
        conn: psycopg2.extensions.connection = psycopg2.connect(
            host="stocks-postgres",
            database="stocks",
            user="postgres",
            password="123456",
            port="5432"
        )
        number_of_companies: int = len(companies_list[0])
        for company_idx in range(1, number_of_companies + 1):
            query: str = f"SELECT trade_date, close FROM stock_prices_main \
            WHERE company_id = {company_idx} ORDER BY trade_date ASC;"
            company_df: pd.DataFrame = pd.read_sql(query, conn)
            company_df["trade_date"] = pd.to_datetime(company_df["trade_date"])
            company_df["trade_date"] = company_df["trade_date"].dt.strftime("%Y-%m-%d")
            company_df["close"] = pd.to_numeric(company_df["close"])
            modified_data: dict = company_df.to_dict("list")
            curr_company_ticker: list = companies_list[0][company_idx - 1]
            companies_data[curr_company_ticker] = modified_data
            # Uncomment below"""This module reads csv data files and processes them into the required format"""

from typing import Union, Tuple
import warnings
import psycopg2  # pylint: disable=E0401
import pandas as pd

warnings.filterwarnings("ignore")


class Model:
    """Processes data and returns data in required format"""

    def __init__(self) -> None:
        self.path: str = "../individual_stocks_5yr/"

    @staticmethod
    def generate_company_list() -> Tuple[list, list]:
        """
        Returns a list of companies.

        :return: (list) A list of companies.
        """
        conn = psycopg2.connect(
            database="stocks",
            user="postgres",
            password="123456",
            port="5432")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM companies;")
        records = cursor.fetchall()
        ticker_list: list = []
        companies_list: list = []
        for row in records:
            (_, ticker, company) = row
            company = company.replace("\xa0", " ")
            ticker_list.append(ticker)
            companies_list.append(company)
        conn.close()
        return ticker_list, companies_list

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

    def process_data(self) -> Union[pd.DataFrame, str]:
        """
        Slices the data as required.

        :return: (DataFrame) A DataFrame containing required information of all companies.
        """
        companies_list: Tuple[list, list] = self.generate_company_list()
        companies_data: dict = {}
        conn: psycopg2.extensions.connection = psycopg2.connect(
            database="stocks", user="postgres", password="123456"
        )
        query: str = f"SELECT company_id, trade_date, close FROM stock_prices_main \
        GROUP BY company_id, trade_date, close ORDER BY trade_date ASC;"
        all_data: pd.DataFrame = pd.read_sql(query, conn)
        grouped_data = all_data.groupby('company_id')[["trade_date", "close"]]
        for company_id, group_data in grouped_data:
            company_df: pd.DataFrame = group_data
            company_df["trade_date"] = pd.to_datetime(company_df["trade_date"])
            company_df["trade_date"] = company_df["trade_date"].dt.strftime("%Y-%m-%d")
            company_df["close"] = pd.to_numeric(company_df["close"])
            modified_data: dict = company_df.to_dict("list")
            curr_company_ticker: list = companies_list[0][company_id - 1]
            companies_data[curr_company_ticker] = modified_data
            # Uncomment below for full company names in selection rather than ticker symbols.
            # curr_company_name = companies_list[1][company_id-1]
            # companies_data[curr_company_name] = modified_data
        all_companies_data: pd.DataFrame = pd.DataFrame(companies_data)
        conn.close()
        return all_companies_data
