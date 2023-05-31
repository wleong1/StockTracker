# TODO:Test coverage: 1. branches(if, else statements and loops), 2.user inputs
# TODO:Delete some data, find out what to do with imperfect data, get ML data
# TODO:SQLite library

API_KEY = "ba1ce03bb02f432ca6f88efb7b475a47"

# mock library

class MainWindow(QMainWindow):
    def __init__(self):
        self.path = "../individual_stocks_5yr/"

    def plot_selected_company(self):
        self.company_name = self.combo_box.currentText()
        converter = ConvertCsvToDict()
        data = converter.convert_to_dict(self.company_name)


class ConvertCsvToDict:
    """Converts the csv files to dictionaries for selected columns"""
    @staticmethod
    def convert_to_dict(filename):
        path = "../individual_stocks_5yr/"
        csv_file_dir = f"{path}{filename}_data.csv"
        df = pd.read_csv(csv_file_dir, header=0, usecols=["date", "open", "high", "low", "close"])
        modified_data = df.to_dict("list")
        return modified_data

class MainWindow(QMainWindow):
    def __init__(self):
        self.path = "../individual_stocks_5yr/"

    def plot_selected_company(self):
        self.company_name = self.combo_box.currentText()
        converter = ConvertCsvToDict()
        data = converter.convert_to_dict(self.path, self.company_name)


class ConvertCsvToDict:
    """Converts the csv files to dictionaries for selected columns"""
    @staticmethod
    def convert_to_dict(path, filename):
        df = pd.read_csv(f"{path}{filename}", header=0, usecols=["date", "open", "high", "low", "close"])
        modified_data = df.to_dict("list")
        return modified_data