import os

from PySide6 import QtWidgets, QtCore, QtGui

from glm.core.qt.singleton_main_window import SingletonMayaMainWindow
from glm.core.qt import ui_loader

from glm.maya.rigging.rig_manager import api

import maya.cmds as cmds

ASSETS_DIR = r'G:\Shared drives\GLM\02_ASSETS'

class RigManagerMainWindow(SingletonMayaMainWindow):

    def __init__(self):
        super().__init__()

        # Load ui
        ui_loader.load_ui(
            os.path.join(os.path.dirname(__file__), 'main_window.ui'),
            self
        )

        self.current_rig_preset:str = list(api.get_rig_presets().keys())[0]

        # Set up rig presets
        self._refresh_rig_presets_combo_box()
        self.rig_preset_combo_box.currentIndexChanged.connect(self._on_rig_presets_combo_box_changed)

        # Set up rig preset settings
        self._refresh_rig_preset_settings()

        self.delete_rig_preset_button.clicked.connect(self._on_delete_rig_preset_button_clicked)

        self.preset_name_line_edit.editingFinished.connect(self._on_preset_name_line_edit_finished)

        self.rig_path_line_edit.editingFinished.connect(self._on_rig_path_line_edit_finished)
        self.rig_path_folder_button.setIcon(QtGui.QIcon(r':\folderPlacholder.png'))
        self.rig_path_folder_button.clicked.connect(self._on_rig_path_folder_button_clicked)

        self.select_deforming_geo_button.clicked.connect(self._on_select_deforming_geo_button_clicked)
        self.replace_deforming_geo_button.clicked.connect(self._on_replace_deforming_geo_button_clicked)

        self.add_model_path_button.clicked.connect(self._on_add_model_path_button_clicked)
        self.remove_model_path_button.clicked.connect(self._on_remove_model_path_button_clicked)

    def refresh_window(self):
        self._refresh_rig_presets_combo_box()
        self._refresh_rig_preset_settings()

    def _refresh_rig_presets_combo_box(self):

        with QtCore.QSignalBlocker(self.rig_preset_combo_box):
            # Clear rig presets combo box
            self.rig_preset_combo_box.clear()

            # Add rig presets to combo box
            rig_presets = api.get_rig_presets()
            rig_preset_names = list(rig_presets.keys())
            self.rig_preset_combo_box.addItems(['(Create Rig Preset)'] + rig_preset_names)

            # Set value in combo box to current rig preset
            self.rig_preset_combo_box.setCurrentIndex(rig_preset_names.index(self.current_rig_preset) + 1)

    def _on_rig_presets_combo_box_changed(self, index: int):

        # If index is 0, create new rig preset
        if index == 0:
            preset_name, success = QtWidgets.QInputDialog.getText(None, 'New Rig Preset', 'Set Preset Name')

            # Return if cancelled
            if not success:
                self.refresh_window()
                return

            rig_presets = api.get_rig_presets()

            # If a preset under the inputted name is empty or already exists, return
            if bool(preset_name.strip()) == False or preset_name in rig_presets.keys():
                print('Error: Invalid Rig Preset Name')
                self.refresh_window()
                return

            rig_info = {
                'Rig Path': '',
                'Model Paths': [],
                'Deforming Geo': []
            }

            rig_presets[preset_name] = rig_info

            api.set_rig_presets(rig_presets)

            self.current_rig_preset = preset_name
            self.refresh_window()

        else:
            # Cache current rig preset
            self.current_rig_preset = self.rig_preset_combo_box.currentText()

            # Reset rig preset settings to match new rig preset selected
            self._refresh_rig_preset_settings()

    def _on_delete_rig_preset_button_clicked(self):

        # Set rig preset
        rig_presets = api.get_rig_presets()
        rig_presets.pop(self.current_rig_preset)

        # Save rig presets
        api.set_rig_presets(rig_presets)
        self.current_rig_preset = list(rig_presets.keys())[0]

        # Refresh window
        self.refresh_window()

    def _refresh_rig_preset_settings(self):

        # Get current rig preset
        rig_preset_info = api.get_rig_presets()[self.current_rig_preset]

        # Set up preset name
        self.preset_name_line_edit.setText(self.current_rig_preset)

        # Set up rig path
        self.rig_path_line_edit.setText(rig_preset_info[api.RIG_PATH_KEY])

        # Set up model paths
        self._refresh_model_paths_list_widget()

    def _refresh_model_paths_list_widget(self):

        # Clear list widget
        self.model_paths_list_widget.clear()

        # Add model paths to list widget
        rig_preset_info = api.get_rig_presets()[self.current_rig_preset]
        self.model_paths_list_widget.addItems(rig_preset_info[api.MODEL_PATHS_KEY])

    def _on_preset_name_line_edit_finished(self):

        # Prevent user from setting the name if it already exists
        rig_presets = api.get_rig_presets()
        if self.preset_name_line_edit.text() in rig_presets:
            with QtCore.QSignalBlocker(self.preset_name_line_edit):
                self.preset_name_line_edit.setText(self.current_rig_preset)

            return

        # Remove preset under old name
        temp_rig_info = rig_presets[self.current_rig_preset]
        rig_presets.pop(self.current_rig_preset)

        # Add preset under new name
        self.current_rig_preset = self.preset_name_line_edit.text()
        rig_presets[self.current_rig_preset] = temp_rig_info

        # Save presets
        api.set_rig_presets(rig_presets)

        self.refresh_window()

    def _on_select_deforming_geo_button_clicked(self):

        # Get the current rig preset deforming geo
        rig_presets = api.get_rig_presets()
        cmds.select(rig_presets[self.current_rig_preset][api.DEFORMING_GEO_KEY])

    def _on_replace_deforming_geo_button_clicked(self):

        # Get selected geo
        selected_geo = cmds.ls(selection=True)

        # Set deforming geo in rig preset info
        rig_presets = api.get_rig_presets()
        rig_preset_info = rig_presets[self.current_rig_preset]
        rig_preset_info[api.DEFORMING_GEO_KEY] = selected_geo

        # Save rig preset
        api.set_rig_presets(rig_presets)

    def _on_rig_path_line_edit_finished(self):

        # Set new rig path in rig preset info
        rig_presets = api.get_rig_presets()
        rig_preset_info = rig_presets[self.current_rig_preset]
        rig_preset_info[api.RIG_PATH_KEY] = self.rig_path_line_edit.text()

        # Save rig presets
        api.set_rig_presets(rig_presets)

        # Refresh Window
        self.refresh_window()


    def _on_rig_path_folder_button_clicked(self):
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,  # parent (ok to pass your QWidget)
            "Select a Rig File",  # title
            ASSETS_DIR,  # starting directory
            "Maya Ascii (*.ma);; Maya Binary (*.mb);; All Files (*)"  # filter
        )

        # If file selected
        if file_path:
            rig_presets = api.get_rig_presets()
            rig_preset_info = rig_presets[self.current_rig_preset]
            rig_preset_info[api.RIG_PATH_KEY] = file_path

            api.set_rig_presets(rig_presets)

            # Refresh Window
            self.refresh_window()

    def _on_add_model_path_button_clicked(self):

        # Open folder
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,  # parent (ok to pass your QWidget)
            "Select a Model File",  # title
            ASSETS_DIR,  # starting directory
            "Maya Ascii (*.ma);; Maya Binary (*.mb);; All Files (*)"  # filter
        )

        # Get the rig preset model paths
        rig_presets = api.get_rig_presets()
        rig_info = rig_presets[self.current_rig_preset]
        model_paths = rig_info[api.MODEL_PATHS_KEY]
        model_paths.append(file_path)

        # Save rig presets
        api.set_rig_presets(rig_presets)

        # Refresh Window
        self.refresh_window()

    def _on_remove_model_path_button_clicked(self):

        # Get selected items in list widget
        selected_items = self.model_paths_list_widget.selectedItems()
        selected_items = set([item.text() for item in selected_items])

        # Get the rig preset model paths
        rig_presets = api.get_rig_presets()
        rig_info = rig_presets[self.current_rig_preset]
        model_paths = set(rig_info[api.MODEL_PATHS_KEY])

        # Set new model paths
        model_paths = list(model_paths - selected_items)
        rig_info[api.MODEL_PATHS_KEY] = model_paths

        # Save rig presets
        api.set_rig_presets(rig_presets)

        # Refresh Window
        self.refresh_window()