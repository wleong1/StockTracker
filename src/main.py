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

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        vbox_right = QVBoxLayout()

        cs: CompanySelection = CompanySelection()

        vbox_right.addWidget(cs.combo_box)
        vbox_right.addWidget(cs.live_price_display_widget.share_price_label)
        vbox_right.addWidget(cs.news_display_widget.company_news_section)

        window_layout = QHBoxLayout()

        window_layout.addLayout(cs.graph_plotting_widget.vbox_left)
        window_layout.addLayout(vbox_right)

        central_widget.setLayout(window_layout)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
