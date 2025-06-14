import os

from PyQt5 import QtWidgets, uic

import styles

class GLMDialog(QtWidgets.QDialog):

    def __init__(self, ui_path, parent=None):
        """ Initialize dialog and UI"""
        super().__init__(parent)

        # Load UI
        uic.loadUi(
            os.path.join(ui_path),
            baseinstance=self
        )

        # Set styles
        self.setStyleSheet(styles.STYLESHEET)

        self.show()