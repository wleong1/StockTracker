from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtWebEngineWidgets import QWebEngineView
from bokeh.plotting import figure
from bokeh.resources import CDN
from bokeh.embed import file_html
from bokeh.models import ColumnDataSource
from data_processing import DataProcessing

import numpy as np
import pandas as pd

PLOT_HEIGHT = 700
PLOT_WIDTH = 1100


class GraphPlotting(QWidget):
    """Plots graph from available data"""
    web_view: QWebEngineView

    def __init__(self, parent=None):
        super().__init__()
        self.web_view: str = None
        self.parent = parent
        self.vbox_left = QVBoxLayout()
        self.placeholder_graph()
        self.data_processor = DataProcessing()

    def placeholder_graph(self) -> None:
        """
        Creates a placeholder graph using Bokeh.

        :return: None
        """
        p = figure()
        p.line([1, 2, 3, 4, 5], [5, 4, 3, 2, 1])

        # Convert the Bokeh plot to HTML
        html: str = file_html(p, CDN, "my plot")

        # Create a web view widget to display the Bokeh plot
        self.web_view = QWebEngineView()
        self.web_view.setHtml(html)

        self.vbox_left.addWidget(self.web_view)

    @staticmethod
    def plotting_data(filename: dict) -> str:
        """
        Obtains the data of the selected company.

        :param filename: (dict) Data of the selected company.
        :return: (str) Html code for graph plotting.
        """
        dates: np.ndarray = np.array(filename["date"], dtype=np.datetime64)
        source: ColumnDataSource = ColumnDataSource(data=dict(date=dates, close=filename["close"]))
        p = figure(height=PLOT_HEIGHT, width=PLOT_WIDTH, tools="xpan, hover", toolbar_location=None,
                   x_axis_type="datetime", x_axis_location="below", x_range=(dates[250], dates[-1]),
                   background_fill_color="#efefef")

        p.line("date", "close", source=source)
        p.yaxis.axis_label = "Price"

        html = file_html(p, CDN, "my_plot")

        return html

    def plot_selected_graph(self, company_name: str) -> None:
        """
        Plots selected company.

        :param company_name: (str) The name of the selected company
        :return: None
        """
        data: dict = self.data_processor.companies_data[company_name].to_dict()
        html = self.plotting_data(data)

        if hasattr(self, 'web_view'):
            self.vbox_left.removeWidget(self.web_view)
            self.web_view.deleteLater()

        # Create a web view widget to display the Bokeh plot
        self.web_view = QWebEngineView()
        self.web_view.setHtml(html)

        self.vbox_left.addWidget(self.web_view)
