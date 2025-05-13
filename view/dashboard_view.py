from PyQt5.QtWidgets import QWidget, QStackedWidget, QVBoxLayout

from .styles.main_styles import NO_MARGINS

class DashboardView(QWidget):

    def __init__(self, parent=None):
        super(DashboardView, self).__init__(parent)

        # Create layout
        self.setLayout(QVBoxLayout())
        self.layout().setContentsMargins(*NO_MARGINS)