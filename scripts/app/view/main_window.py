from PyQt5.QtWidgets import QMainWindow, QWidget
from PyQt5.QtWidgets.QMainWindow import centralWidget


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set up window
        self.setWindowTitle('GLM Pipeline Hub')

        # Set up central widget
        central_widget = QWidget(self)
        central_widget.setLayout()

        self.setCentralWidget(central_widget)
