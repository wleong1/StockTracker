"""This module processes raw data and returns processed data in required format."""
from typing import Union, Tuple
import warnings
import psycopg2  # pylint: disable=E0401
from sqlalchemy.engine import URL
from sqlalchemy import create_engine, MetaData, Column, Integer, Numeric, Date, String, ForeignKey, BigInteger, func
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import sessionmaker, mapper, declarative_base, relationship
import pandas as pd

warnings.filterwarnings("ignore")


class Model:
    """Processes data and returns data in required format"""

    def __init__(self) -> None:
        """
        Constructs all the necessary attributes to make the necessary connection to the
        database.

        Args:
            None

        Returns:
            None
        """
        self.path: str = "../individual_stocks_5yr/"
        self.params: dict = {"host":"pgbouncer",
                             "database":"stocks",
                             "user":"postgres",
                             "password":"123456",
                             "port":"6432"}
        # self.params: dict = {"database":"stocks",
        #                      "user":"postgres",
        #                      "password":"123456",
        #                      "port":"6432"}

    def generate_company_list(self) -> Tuple[list, list]:
        """
        Returns a list of companies.

        Args:
            None

        Returns:
            A list of companies.
        """

        connection_string = f"postgresql://{self.params['user']}:{self.params['password']}@{self.params['host']}:{self.params['port']}/{self.params['database']}"
        # connection_string = f"postgresql://{self.params['user']}:{self.params['password']}@localhost:{self.params['port']}/{self.params['database']}"
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        session = Session()

        rows = session.query(Company).all()
        ticker_list: list = []
        companies_list: list = []

        for row in rows:
            ticker_list.append(row.ticker)
            companies_list.append(row.company_name)

        session.commit()
        session.close()

        return ticker_list, companies_list

    def check_headers_and_data(self, file: str, expected_headers: list) -> bool:
        """
        Checks if each csv file has the expected headers and at least one data point for each header

        Args:
            file: The name of the file being checked
            expected_headers: The list of headers required

        Returns:
            The results of the file
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

    def process_data(self, company_name: str) -> Union[pd.DataFrame, str]:
        """
        Slices the data as required.

        Args:
            None

        Returns:
            A DataFrame containing required information of all companies.
        """
        # connection_string = f"postgresql://{self.params['user']}:{self.params['password']}@localhost:{self.params['port']}/{self.params['database']}"
        connection_string = f"postgresql://{self.params['user']}:{self.params['password']}@{self.params['host']}:{self.params['port']}/{self.params['database']}"
        engine = create_engine(connection_string)
        Session = sessionmaker(bind=engine)
        session = Session()

        # Perform the ORM query
        query = (
            session.query(StockPrice, Company)
            .join(Company, StockPrice.company_id == Company.company_id)
            .filter(Company.ticker == company_name)
        )

        # Execute the query and fetch results
        results = query.all()
        trade_date: list = []
        close_price: list = []
        for stock_price, _ in results:
            trade_date.append(pd.to_datetime(stock_price.trade_date).strftime("%Y-%m-%d"))
            close_price.append(pd.to_numeric(stock_price.close))
        session.close()
        return trade_date, close_price

Base = declarative_base()

class StockPrice(Base):
    __tablename__ = 'stock_prices'
    price_id = Column(BigInteger, primary_key=True)
    company_id = Column(Integer, ForeignKey('companies.company_id'), nullable=False)
    trade_date = Column(Date, nullable=False)
    open = Column(Numeric(10, 4), nullable=False)
    high = Column(Numeric(10, 4), nullable=False)
    low = Column(Numeric(10, 4), nullable=False)
    close = Column(Numeric(10, 4), nullable=False)
    volume = Column(BigInteger, nullable=False)
    company = relationship('Company', back_populates='stock_prices')

# Define the Company class
class Company(Base):
    __tablename__ = 'companies'
    company_id = Column(Integer, primary_key=True)
    ticker = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    stock_prices = relationship('StockPrice', back_populates='company')

print(Model().generate_company_list())