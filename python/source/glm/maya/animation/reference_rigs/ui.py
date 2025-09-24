import os

from PySide6 import QtWidgets

from glm.core.qt.singleton_main_window import SingletonMayaMainWindow
from glm.core.qt import ui_loader

from glm.maya.animation.reference_rigs import api
from glm.maya.rigging.rig_manager import api as rig_manager

class ReferenceRigsMainWindow(SingletonMayaMainWindow):

    def __init__(self):
        super().__init__()

        # Load UI
        ui_loader.load_ui(os.path.join(
            os.path.abspath(os.path.dirname(__file__)), 'main_window.ui'),
            self
        )

        # Set up add rig button
        self.add_rig_button.clicked.connect(self._on_add_rig_button_clicked)

        # Set up remove rig button
        self.remove_rig_button.clicked.connect(self._on_remove_rig_button_clicked)

        # Set up rig references list widget
        self._refresh_rig_references_list_widget()

    def _on_add_rig_button_clicked(self):

        # Select Rigs to Import
        SelectRigsDialog().exec_()

        # Refresh ui
        self._refresh_rig_references_list_widget()

    def _on_remove_rig_button_clicked(self):
        selected_items = self.rig_references_list_widget.selectedItems()
        selected_items = [item.text() for item in selected_items]

        api.remove_rig_references_by_namespace(selected_items)

        # Refresh ui
        self._refresh_rig_references_list_widget()

    def _refresh_rig_references_list_widget(self):
        # Clear list widget
        self.rig_references_list_widget.clear()

        # Add items to list widget
        self.rig_references_list_widget.addItems(api.get_rig_reference_namespaces_without_prefix())

class SelectRigsDialog(QtWidgets.QDialog):

    def __init__(self):
        super().__init__()

        # Load UI
        ui_loader.load_ui(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), 'select_rigs_dialog.ui') ,
            self
        )

        # Set up rig list widget
        self._refresh_rig_list_widget()

        # Set up reference selected rigs button
        self.reference_selected_rigs_button.clicked.connect(self._on_reference_selected_rigs_button)

    def _refresh_rig_list_widget(self):

        # Clear widget
        self.rig_list_widget.clear()

        # Add items to widget
        rig_presets = list(rig_manager.get_rig_presets().keys())
        self.rig_list_widget.addItems(rig_presets)


    def _on_reference_selected_rigs_button(self):
        selected_items = self.rig_list_widget.selectedItems()
        selected_items = [item.text() for item in selected_items]

        for item in selected_items:
            namespace = item
            rig_preset_info = rig_manager.get_rig_presets()[namespace]
            rig_path = rig_preset_info[rig_manager.RIG_PATH_KEY]

            if os.path.exists(rig_path):
                api.add_rig_reference(rig_path, namespace)
            else:
                print('Error: Rig path does not exist')

            self.close()