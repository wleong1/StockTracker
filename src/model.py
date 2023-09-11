from os import walk
import csv


class Model:
    """Processes data and returns data in required format"""
    def __init__(self, parent=None):
        super().__init__()
        self.company_list = None
        self.parent = parent
        self.path: str = "../individual_stocks_5yr/"
        self.generate_company_list()

    def generate_company_list(self) -> list:
        """
        Returns a list of companies.

        :return: (list) A list of companies.
        """
        self.company_list: list = []
        expected_headers = ["date", "close"]
        for (dirpath, dirnames, filenames) in walk(self.path):
            for file in filenames:
                if file.endswith(".csv"):
                    if self.check_headers_and_data(file, expected_headers):
                        company_name: str = file[:-9]
                        self.company_list.append(company_name)
        self.company_list.sort()
        return self.company_list

    def check_headers_and_data(self, filename, expected_headers) -> bool:
        """
        Checks if each csv file has the expected headers and at least one data point for each header
        :param filename: (str) The name of the file being checked
        :param expected_headers: (list) The list of headers required
        :return: (bool) The results of the file
        """
        has_expected_headers = False
        has_data = False

        with open(self.path + filename, 'r', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for header in expected_headers:
                    if row.get(header):
                        has_expected_headers = True
                        has_data = True
                        break
                if has_expected_headers and has_data:
                    break
        return has_expected_headers and has_data
