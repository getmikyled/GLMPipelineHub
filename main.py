import sys

from PyQt5 import QtWidgets

from glm_pipeline_hub.ui import GLMPipelineHubMainWindow
from styles import STYLESHEET


def main():
    sys.path.append(r'G:\Shared drives\GLM\06_PIPELINE\python\source')

    app = QtWidgets.QApplication(sys.argv)
    app.setStyleSheet(STYLESHEET)

    main_window = GLMPipelineHubMainWindow()

    app.exec_()


def on_start():
    pass

if __name__ == '__main__':
    main()