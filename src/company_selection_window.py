from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
import sys

class CompanySelectionWindow(QWidget):
    """Creates a window that allows user to select the company"""
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.label = QLabel("Another window")
        layout.addWidget(self.label)
        self.setLayout(layout)
