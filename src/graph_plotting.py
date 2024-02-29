from PyQt5.QtWidgets import QWidget, QVBoxLayout
import pyqtgraph as pg
import os, sys
sys.path.append(os.getcwd())
from processing.data_processing import DataProcessing

import numpy as np
import pandas as pd

PLOT_HEIGHT = 700
PLOT_WIDTH = 1100


class GraphPlotting(QWidget):
    """Plots graph from available data"""

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
        self.plot = pg.PlotWidget()
        self.x = [1, 2, 3, 4, 5]
        self.y = [5, 4, 3, 2, 1]

        self.dataline = self.plot.plot(self.x, self.y)
        self.vbox_left.addWidget(self.plot)

        return self.plot

    def plot_selected_graph(self, company_name: str) -> None:
        """
        Plots selected company.

        :param company_name: (str) The name of the selected company
        :return: None
        """
        data: dict = self.data_processor.companies_data[company_name].to_dict()
        self.x = data["date"]
        self.y = data["close"]
        # print(self.x)
        # print(self.y)
        # print(len(self.x)==len(self.y))
        # self.dataline.setData(self.x, self.y)