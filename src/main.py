from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QApplication, QHBoxLayout
import sys

from company_selection import CompanySelection


class MainWindow(QMainWindow):
    """Main GUI window"""

    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setWindowTitle("Stock Viewer")
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()

        # Create a central widget for the main window
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Create a vertical layout for the right side of the window
        vbox_right = QVBoxLayout()

        # Create an instance of CompanySelection widget
        cs = CompanySelection()

        # Add the combo box, live price label, and news section to the right side layout
        vbox_right.addWidget(cs.combo_box)
        vbox_right.addWidget(cs.live_price_display_widget.share_price_label)
        vbox_right.addWidget(cs.news_display_widget.company_news_section)

        # Create a horizontal layout for the main window
        window_layout = QHBoxLayout()

        # Add the graph plotting layout and right side layout to the main window layout
        window_layout.addLayout(cs.graph_plotting_widget.vbox_left)
        window_layout.addLayout(vbox_right)

        # Set the main window layout as the layout for the central widget
        central_widget.setLayout(window_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
