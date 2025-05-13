from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QStackedWidget

from view.styles.main_styles import MAIN_STYLES, NO_MARGINS


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Set up window
        self.setWindowTitle('GLM Pipeline Hub')

        # Set up central widget
        central_widget = QWidget(self)
        central_widget.setLayout(QVBoxLayout())
        central_widget.layout().setContentsMargins(*NO_MARGINS)
        self.setCentralWidget(central_widget)

        # Create widget stack. Holds all pages for the application
        self.stack = QStackedWidget()
        self.stack.setStyleSheet(MAIN_STYLES)
        self.centralWidget().layout().addWidget(self.stack)