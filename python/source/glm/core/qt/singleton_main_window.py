# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import os
from shiboken6 import wrapInstance

from PySide6 import QtWidgets, QtGui

import maya.OpenMayaUI as omui

import sitecustomize

__all__ = ['SingletonMayaMainWindow']

def get_maya_main_window():
    main_window_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

class SingletonMayaMainWindow(QtWidgets.QMainWindow):
    _instance = None  # Singleton instance

    def __new__(cls):

        # Close if window is already opened
        if cls._instance is not None:
            cls._instance.close()
            cls._instance.deleteLater()
            cls._instance = None

        # Create and return new instance
        cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        super().__init__(parent=get_maya_main_window())
        if getattr(self, "_initialized", False):
            return

        self._initialized = True
        self.setWindowIcon(QtGui.QIcon(os.path.join(sitecustomize.IMAGES_DIR, 'glm_icon.jpg')))