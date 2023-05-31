from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout # Need to use PyQt5 due to error below
from PyQt5.QtWebEngineWidgets import QWebEngineView # Don't know why PyQt6 does not have QtWebEngineWidgets
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from converting_data import convert_csv_to_dict
from visualise_data import VisualiseData
import sys

STOCK_NAME = "GOOGL"
c = convert_csv_to_dict()
p = c.convert_to_dict(STOCK_NAME)

v = VisualiseData()
v.plotting_data(p)

# TODO:Convert all files into dict format

class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # # Create a Bokeh plot
        # p = figure(width=400, height=400)
        # p.line([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])
        #
        # # Convert the Bokeh plot to HTML
        # html = file_html(p, CDN, "my plot")

        # Create a web view widget to display the Bokeh plot

        STOCK_NAME = "GOOGL"
        c = convert_csv_to_dict()
        p = c.convert_to_dict(STOCK_NAME)

        v = VisualiseData()
        html = v.plotting_data(p)

        web_view = QWebEngineView()
        web_view.setHtml(html)

        # Add the web view widget to a layout
        layout = QVBoxLayout()
        layout.addWidget(web_view)

        # Create a central widget to hold the layout
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set the central widget of the main window
        self.setCentralWidget(central_widget)


app = QApplication(sys.argv)
window = MyMainWindow()
window.show()
app.exec_()
