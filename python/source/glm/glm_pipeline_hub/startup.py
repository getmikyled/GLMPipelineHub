# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import sys

from PyQt5 import QtWidgets

from glm.glm_pipeline_hub import substance_painter
from ui import GLMPipelineHubMainWindow
from styles import STYLESHEET


MODULES = [
    substance_painter
]

def startup():
    for module in MODULES:
        module.startup()

    # Launch Pipeline Hub
    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)

    main_window = GLMPipelineHubMainWindow()

    app.exec_()

if __name__ == '__main__':
    startup()