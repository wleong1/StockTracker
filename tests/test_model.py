import unittest
from src import model

class MyModelTestCase(unittest.TestCase):

    def test_generate_company_list(self):
        """
        Test the model functionality.

        This test case checks if the model works correctly by comparing
        the final list of companies with the expected list of companies.

        :return: None
        """
        model_test = model.Model()
        model_test.path = "sample_data/"
        company_list = model_test.generate_company_list()

        self.assertEqual(company_list, ["CompanyA", "CompanyB", "CompanyC", "CompanyD"])


if __name__ == '__main__':
    unittest.main()