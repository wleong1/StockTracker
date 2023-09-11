import unittest
import sys

pkg_dir = "../src"
sys.path.append(pkg_dir)

from src import data_processing, model


class MyDataProcessingTestCase(unittest.TestCase):

    def test_process_data(self):
        """
        Test the data processing functionality.

        This test case checks if the data processing works correctly by comparing
        the number of data points generated for each company.

        :return: None
        """

        data_processor = data_processing.DataProcessing()
        model_test = model.Model()
        model_test.path = "sample_data/"
        company_list = model_test.generate_company_list()

        data_processor.companies_list = company_list
        data_processor.path = "sample_data/"
        test_data = data_processor.process_data()

        companies_passed = []
        for company in company_list:
            if len(test_data[company]) == 2:
                companies_passed.append(company)
        self.assertEqual(company_list, companies_passed)


if __name__ == '__main__':
    unittest.main()
