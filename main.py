import sys
from PyQt5.QtWidgets import QApplication
from controller import MainController

def main():
    # Create app
    app = QApplication(sys.argv)

    # Create the window
    main_controller = MainController()
    window = main_controller.view

    window.showMaximized()
    sys.exit(app.exec_())

def on_start():
    pass

if __name__ == '__main__':
    main()