from PyQt5.QtWidgets import QWidget, QComboBox
from os import walk

from news_display import NewsDisplay
from graph_plotting import GraphPlotting
from live_price_display import LivePriceDisplay
from data_processing import DataProcessing


class CompanySelection(QWidget):
    """Displays and handles company selection menu"""

    def __init__(self, parent=None):
        super().__init__()
        self.path = DataProcessing().path
        self.parent = parent
        self.combo_box = QComboBox()
        self.combo_box.setMaximumSize(700, 50)
        self.combo_box.addItem("Select a company")

        # Populate the combo box with available company names from csv files
        for (dirpath, dirnames, filenames) in walk(self.path):
            for file in filenames:
                if file.endswith(".csv"):
                    self.combo_box.addItem(file[:-9])

        # Create instances of widgets for graph plotting, live price display, and news display
        self.graph_plotting_widget = GraphPlotting()
        self.live_price_display_widget = LivePriceDisplay()
        self.news_display_widget = NewsDisplay()

        # Connect the combo box's currentTextChanged signal to update the selected company in the widgets
        self.combo_box.currentTextChanged.connect(lambda: self.graph_plotting_widget.plot_selected_graph(
            self.combo_box.currentText()))
        self.combo_box.currentTextChanged.connect(lambda: self.live_price_display_widget.display_final_price(
            self.combo_box.currentText()))
        self.combo_box.currentTextChanged.connect(lambda: self.news_display_widget.display_company_news(
            self.combo_box.currentText()))
