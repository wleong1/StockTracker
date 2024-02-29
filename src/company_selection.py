from PyQt5.QtWidgets import QWidget, QComboBox
from graph_plotting import GraphPlotting
from live_price_display import LivePriceDisplay
from news_display import NewsDisplay
from models.model import Model

class CompanySelection(QWidget):
    """Displays and handles company selection menu"""

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.combo_box = QComboBox()
        self.combo_box.setMaximumSize(700, 50)
        self.placeholder_text: str = "Select a company"
        self.combo_box.addItem(self.placeholder_text)

        models = Model()
        # Populate the combo box with available company names from csv files
        for company in models.company_list:
            self.combo_box.addItem(company)

        # Create instances of widgets for graph plotting, live price display, and news display
        self.graph_plotting_widget: GraphPlotting = GraphPlotting()
        self.live_price_display_widget: LivePriceDisplay = LivePriceDisplay()
        self.news_display_widget: NewsDisplay = NewsDisplay()
        self.combo_box.currentTextChanged.connect(lambda: self.company_selected())

        # Connect the combo box's currentTextChanged signal to update the selected company in the widgets
    def company_selected(self) -> None:
        """
        If the selected company is not equal to the placeholder text, it will obtain information of the selected company
        , if it is then it will not do anything.

        :return: None
        """
        if self.combo_box.currentText() != self.placeholder_text:
            self.graph_plotting_widget.plot_selected_graph(self.combo_box.currentText())
            self.live_price_display_widget.display_final_price(self.combo_box.currentText())
            self.news_display_widget.display_company_news(self.combo_box.currentText())
