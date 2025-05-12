import sys
from PyQt5.QtWidgets import QApplication
from scripts.app.view import MainWindow

def main():
    # Create app
    app = QApplication(sys.argv)

    # Create the window
    window = MainWindow()
    window.showMaximized()

    sys.exit(app.exec_())

def on_start():
    pass

main()