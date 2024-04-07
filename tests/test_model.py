import pytest
from src import model
from unittest.mock import patch, Mock
import pandas as pd

@pytest.fixture
def test_model():
    yield model.Model()

@patch("src.model.Model.check_headers_and_data")
@patch("os.walk")
def test_generate_company_list(mock_walk, mock_check_headers_and_data, test_model):
    mock_walk.return_value = [(" ", " ", ['CompanyB_data.csv', 'CompanyE_data.xml', 'CompanyA_data.csv',
                      'CompanyF_data.xlsx', 'CompanyD_data.csv', 'CompanyC_data.csv',
                      'CompanyD_data.txt'])]
    mock_check_headers_and_data.return_value = True
    company_list = test_model.generate_company_list()
    assert company_list == ["CompanyA", "CompanyB", "CompanyC", "CompanyD"]

@pytest.fixture
def test_headers():
    yield ["date", "close"]

@pytest.fixture
def dummy_data_all_true():
    data = [["date", "close"],
            ["2023-12-12", 219.87]]
    df = pd.DataFrame(data[1:], columns=data[0])
    yield df

@patch("pandas.read_csv")
def test_check_headers_and_data_all_true(mock_read_csv, test_model, dummy_data_all_true):
    mock_read_csv.return_value = dummy_data_all_true
    expected_headers = ["date", "close"]
    results = test_model.check_headers_and_data("", expected_headers=expected_headers)
    assert results == True

@pytest.fixture
def dummy_data_expected_headers_not_met():
    data = [["date", "open"],
            ["2023-12-12", 219.87]]
    df = pd.DataFrame(data[1:], columns=data[0])
    yield df

@patch("pandas.read_csv")
def test_check_headers_and_data_false_headers_true_data(mock_read_csv, test_model, dummy_data_expected_headers_not_met):
    mock_read_csv.return_value = dummy_data_expected_headers_not_met
    expected_headers = ["date", "close"]
    results = test_model.check_headers_and_data("", expected_headers=expected_headers)
    assert results == False

@pytest.fixture
def dummy_data_only_headers():
    data = [["date", "close"]]
    df = pd.DataFrame(columns=data[0])
    yield df

@patch("pandas.read_csv")
def test_check_headers_and_data_only_headers(mock_read_csv, test_model, dummy_data_only_headers):
    mock_read_csv.return_value = dummy_data_only_headers
    expected_headers = ["date", "close"]
    results = test_model.check_headers_and_data("", expected_headers=expected_headers)
    assert results == False

@pytest.fixture
def dummy_data_only_data():
    data = [["2023-12-12", 219.87]]
    df = pd.DataFrame(data[0])
    yield df

@patch("pandas.read_csv")
def test_check_headers_and_data_only_data(mock_read_csv, test_model, dummy_data_only_data):
    mock_read_csv.return_value = dummy_data_only_data
    expected_headers = ["date", "close"]
    results = test_model.check_headers_and_data("", expected_headers=expected_headers)
    assert results == False

@pytest.fixture
def dummy_data_empty_csv():
    df = pd.DataFrame()
    yield df

@patch("pandas.read_csv")
def test_check_headers_and_data_empty_csv(mock_read_csv, test_model, dummy_data_empty_csv):
    mock_read_csv.return_value = dummy_data_empty_csv
    expected_headers = ["date", "close"]
    results = test_model.check_headers_and_data("", expected_headers=expected_headers)
    assert results == False

@pytest.fixture
def dummy_data_additional_headers():
    data = [["date", "open", "close", "high", "low"],
            ["2023-12-12", 219.87, 123, 245, 112]]
    df = pd.DataFrame(data[1:], columns=data[0])
    yield df

@patch("pandas.read_csv")
def test_check_headers_and_data_additional_headers(mock_read_csv, test_model, dummy_data_additional_headers):
    mock_read_csv.return_value = dummy_data_additional_headers
    expected_headers = ["date", "close"]
    results = test_model.check_headers_and_data("", expected_headers=expected_headers)
    assert results == True

@pytest.fixture
def dummy_data_different_order_headers():
    data = [["close", "open", "date", "high", "low"],
            [123, 219.87, "2023-12-12", 245, 112]]
    df = pd.DataFrame(data[1:], columns=data[0])
    yield df

@patch("pandas.read_csv")
def test_check_headers_and_data_different_order_headers(mock_read_csv, test_model, dummy_data_different_order_headers):
    mock_read_csv.return_value = dummy_data_different_order_headers
    expected_headers = ["date", "close"]
    results = test_model.check_headers_and_data("", expected_headers=expected_headers)
    assert results == True

@pytest.fixture
def dummy_data_wrong_position_headers():
    data = [["2023-12-12", 219.87],
            ["date", "close"]]
    df = pd.DataFrame(data[1:], columns=data[0])
    yield df

@patch("pandas.read_csv")
def test_check_headers_and_data_wrong_position_headers(mock_read_csv, test_model, dummy_data_wrong_position_headers):
    mock_read_csv.return_value = dummy_data_wrong_position_headers
    expected_headers = ["date", "close"]
    results = test_model.check_headers_and_data("", expected_headers=expected_headers)
    assert results == False

@patch("src.model.Model.generate_company_list")
@patch("pandas.read_csv")
def test_process_data_all_true(mock_read_csv, mock_company_list, test_model, dummy_data_all_true):
    mock_company_list.return_value = ["Company_A"]
    mock_read_csv.return_value = dummy_data_all_true
    results = test_model.process_data(["date", "close"])
    assert isinstance(results, pd.DataFrame)
    assert (results["Company_A"]["date"] == ["2023-12-12"] and results["Company_A"]["close"] == [219.87])

@pytest.fixture
def dummy_data_repeated_headers_date():
    data = [["date", "date", "close"],
            ["2023-12-12", "2023-12-11", 219.87]]
    df = pd.DataFrame(data[1:], columns=data[0])
    yield df

@patch("src.model.Model.generate_company_list")
@patch("pandas.read_csv")
def test_process_data_repeated_headers_date_value_error(mock_read_csv, mock_company_list, test_model, dummy_data_repeated_headers_date):
    mock_company_list.return_value = ["Company_A"]
    mock_read_csv.return_value = dummy_data_repeated_headers_date
    results = test_model.process_data(["date", "close"])
    assert isinstance(results, str)
    assert results == "Please ensure each header is unique, data is correct, or expected_headers and process_data are configured correctly"

@pytest.fixture
def dummy_data_repeated_headers_close():
    data = [["date", "close", "close"],
            ["2023-12-12", 219.87, 912.87]]
    df = pd.DataFrame(data[1:], columns=data[0])
    yield df

@patch("src.model.Model.generate_company_list")
@patch("pandas.read_csv")
def test_process_data_repeated_headers_close_type_error(mock_read_csv, mock_company_list, test_model, dummy_data_repeated_headers_close):
    mock_company_list.return_value = ["Company_A"]
    mock_read_csv.return_value = dummy_data_repeated_headers_close
    results = test_model.process_data(["date", "close"])
    assert isinstance(results, str)
    assert results == "Please ensure each header is unique, data is correct, or expected_headers and process_data are configured correctly"

@pytest.fixture
def dummy_data_key_error():
    data = [["date", "date"],
            ["2023-12-12", "2023-12-12"]]
    df = pd.DataFrame(data[1:], columns=data[0])
    yield df

@patch("src.model.Model.generate_company_list")
@patch("pandas.read_csv")
def test_process_data_key_error(mock_read_csv, mock_company_list, test_model, dummy_data_key_error):
    mock_company_list.return_value = ["Company_A"]
    mock_read_csv.return_value = dummy_data_key_error
    results = test_model.process_data(["close", "close"])
    assert isinstance(results, str)
    assert results == "Please ensure each header is unique, data is correct, or expected_headers and process_data are configured correctly"
