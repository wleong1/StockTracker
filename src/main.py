from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from PyQt5.QtWebEngineWidgets import QWebEngineView

from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html

from converting_data import ConvertCsvToDict
from visualise_data import VisualiseData
from news_collector import NewsCollector

from os import walk
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.web_view = None
        self.company_name = None
        self.combo_box = None
        self.company_news_section = None
        self.share_price_label = None
        self.live_data = None
        self.company_news = None
        self.news_label = None
        self.path = "../individual_stocks_5yr/"

        self.setWindowTitle("Stock Viewer")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Create layouts
        self.vbox_right = QVBoxLayout()
        self.vbox_left = QVBoxLayout()
        self.hbox_graph = QHBoxLayout()
        self.vbox_news = QVBoxLayout()
        self.hbox_window = QHBoxLayout()

        self.vbox_left.addLayout(self.hbox_graph)

        # Create widgets
        self.placeholder()
        self.display_company_menu()
        self.display_company_news()
        self.display_live_price()

        # Add widgets to layout
        self.vbox_right.addWidget(self.combo_box)
        self.vbox_right.addWidget(self.share_price_label)
        self.vbox_right.addWidget(self.company_news_section)

        self.hbox_window.addLayout(self.vbox_left)
        self.hbox_window.addLayout(self.vbox_right)

        self.central_widget.setLayout(self.hbox_window)

    # Placeholder graph
    def placeholder(self): #TODO:MAKE GRAPH WITHOUT USING BOKEH, USE PYQT INBUILT PLOTTING METHOD INSTEAD
        p = figure()
        p.line([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])

        # Convert the Bokeh plot to HTML
        html = file_html(p, CDN, "my plot")

        # Create a web view widget to display the Bokeh plot
        self.web_view = QWebEngineView()
        self.web_view.setHtml(html)

        self.vbox_left.addWidget(self.web_view)

    # Graph
    def plot_selected_company(self):
        self.company_name = self.combo_box.currentText()
        converter = ConvertCsvToDict()
        data = converter.convert_to_dict(self.company_name)

        visualiser = VisualiseData()
        html = visualiser.plotting_data(data)

        if hasattr(self, 'web_view'):
            self.vbox_left.removeWidget(self.web_view)
            self.web_view.deleteLater()

        # Create a web view widget to display the Bokeh plot
        self.web_view = QWebEngineView()
        self.web_view.setHtml(html)

        self.vbox_left.addWidget(self.web_view)

    # Company selection
    def display_company_menu(self):
        self.combo_box = QComboBox()
        self.combo_box.setMaximumSize(700, 50)
        self.combo_box.addItem("Select a company")
        for (dirpath, dirnames, filenames) in walk(self.path):
            for file in filenames:
                if file.endswith(".csv"):
                    self.combo_box.addItem(file[:-9])
        self.combo_box.currentTextChanged.connect(self.plot_selected_company)
        self.combo_box.currentTextChanged.connect(self.display_final_price)
        self.combo_box.currentTextChanged.connect(self.display_recent_news)

    # Recent news
    def display_company_news(self):
        self.company_news_section = QGroupBox("Live news")
        self.company_news_section.setMaximumSize(700, 500)
        self.company_news_section.setFont(QFont("Times", 9))

    # Live data
    def display_live_price(self):
        self.share_price_label = QLabel("Live price")
        self.share_price_label.setMaximumSize(700, 500)
        self.share_price_label.setFont(QFont("Times", 24))
        self.share_price_label.setAlignment(QtCore.Qt.AlignCenter)

    def display_final_price(self):
        self.live_data = ConvertCsvToDict().display_live_data(filename=self.company_name)
        self.share_price_label.setText(f"{self.company_name}:\n{self.live_data}")

    def display_recent_news(self):
        self.company_news = NewsCollector().collect_news(company=self.company_name)
        # Remove news from previously selected company, if any
        while self.vbox_news.count():
            item = self.vbox_news.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()

        # Add news from currently selected company, if any
        for headline in self.company_news:
            self.news_label = QLabel(headline)
            self.news_label.setWordWrap(True)
            self.vbox_news.addWidget(self.news_label)
        self.company_news_section.setLayout(self.vbox_news)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
