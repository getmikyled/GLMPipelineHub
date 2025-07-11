# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import os

from PyQt5 import QtWidgets, uic, QtGui
from Qt import GLMDialog

import glm.glm_pipeline_hub
import glm_pipeline_hub.core.os_utility as os_util
import glm_pipeline_hub.api as api

import glm_pipeline_hub.users.users_utility as users_util

__all__ = ['GLMPipelineHubMainWindow']

SHOTS_DIR = 'G:/Shared drives/GLM/03_SHOTS'
SHOT_BLACKLIST = ['TEMPLATE']

DISABLE = [
    'nuke_launcher_button', 'shot_manager_button'
]

DEPARTMENTS = ['PREVIS_LAYOUT', 'ANIM', 'FINAL_LAYOUT', 'LIGHT', 'FX_CFX', 'COMP']

class GLMPipelineHubMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        # Load UI
        uic.loadUi(
            os_util.get_resource_path(r'resources\ui\main_window.ui'),
            baseinstance=self
        )

        self.show()

        self._init_user()
        self._init_ui()

        glm.glm_pipeline_hub.startup()

    def _init_ui(self):
        """ Initialize the window's UI."""

        # -------------------------------------------
        # Disable desired widgets
        for name in DISABLE:
            widget = getattr(self, name, None)
            if widget:
                widget.setVisible(False)
            else:
                print(f'Warning: {name} not found')

        # -------------------------------------------
        # Sidebar setup

        self.app_launcher_button.clicked.connect(lambda: self.stack.setCurrentIndex(0))
        self.shot_manager_button.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        self.system_profile_button.clicked.connect(lambda: self.stack.setCurrentIndex(2))

        # -------------------------------------------
        # App Launcher Setup

        self.maya_launcher_button.setIcon(
            QtGui.QIcon(os_util.get_resource_path(r'resources\images\icons\maya.png')))
        self.maya_launcher_button.clicked.connect(api.launch_maya)
        self.blender_launcher_button.clicked.connect(api.launch_blender)
        self.blender_launcher_button.setIcon(
            QtGui.QIcon(os_util.get_resource_path(r'resources\images\icons\blender.png')))

        # -------------------------------------------
        # Shot manager setup

        # Shot setup
        self.shot_combo_box.addItems(self._get_shots())

        # Department setup
        self.department_combo_box.addItems(DEPARTMENTS)

        # Select shot buttons setup

        # Set buttons to 50% opacity if disabled
        effect = QtWidgets.QGraphicsOpacityEffect()
        effect.setOpacity(0.5)
        if self.maya_shot_manager_button.isEnabled() == False:
            self.maya_shot_manager_button.setGraphicsEffect(effect)
        if self.blender_shot_manager_button.isEnabled() == False:
            self.blender_shot_manager_button.setGraphicsEffect(effect)
        if self.nuke_shot_manager_button.isEnabled() == False:
            self.nuke_shot_manager_button.setGraphicsEffect(effect)
        if self.render_shot_button.isEnabled() == False:
            self.render_shot_button.setGraphicsEffect(effect)

        # -------------------------------------------
        # System profile setup

        machine_id = users_util.get_machine_id()

        # Username setup

        self.username_line_edit.setText(users_util.get_users()[machine_id]['username'])
        self.edit_username_button.clicked.connect(self._edit_username)

        # Machine ID setup
        self.user_machine_id_label.setText(machine_id)

    def _init_user(self):
        """ Initialize the user of the application."""

        # Check if the machine has already been registered
        users = users_util.get_users()
        self.machine_id = users_util.get_machine_id()

        # If the user has not been registered
        if self.machine_id not in users.keys():
            # Add the user
            users_util.add_user(self.machine_id)

            username = self._input_new_username(force=True)
            users_util.set_user_attr(self.machine_id, 'username', username)

            maya_path = os.path.join(r'C:\Program Files\Autodesk\Maya2024')
            if os.path.exists(maya_path) == False:
                maya_path = self._input_new_path(software='Maya', force=True)
            users_util.set_user_attr(self.machine_id, 'maya_path', maya_path)

            blender_path = os.path.join(r'G:\Shared drives\GLM\06_Pipeline\Blender')
            if os.path.exists(blender_path) == False:
                blender_path = self._input_new_path(software='Blender', force=True)
            users_util.set_user_attr(self.machine_id, 'blender_path', blender_path)

    def _get_shots(self):
        shots = os.listdir(SHOTS_DIR)
        return [dir for dir in shots if (os.path.isdir(f'{SHOTS_DIR}/{dir}') and dir not in SHOT_BLACKLIST)]

    def _input_new_username(self, force : bool) -> str:
        """ Prompt the user to set a new username to be associated with their machine.

        Args:
            force (bool): If true, forces the user to set a new username.

        Returns:
            str: The username that the user set.
        """

        dialog = NewUserDialog()
        result = dialog.exec_()

        # If username saved
        if result == QtWidgets.QDialog.Accepted:
            return dialog.username_line_edit.text()

        else:
            if force:
                # Recursively launch the new first time user setup again
                return self._input_new_username()
        return ''

    def _edit_username(self):
        username = self._input_new_username(force=False)

        if username:
            users_util.set_user_attr(self.machine_id, 'username', username)
            self.username_line_edit.setText(username)

    def _input_new_path(self, software : str, force : bool) -> str:
        """ Prompt the user to input a new path.

        Args:
            software (str): The name of the software that the user is being prompted a path for.
            force (bool): If true, forces the user to set a new path.
        """

        dialog = SetPathDialog(software=software, path=r'C:\Program Files')
        result = dialog.exec_()

        # If path saved
        if result == QtWidgets.QDialog.Accepted:
            return dialog.path_line_edit.text()
        else:
            if force:
                # Recursively launch the new first time user setup again
                return self._input_new_path()
        return ''


class NewUserDialog(GLMDialog):

    def __init__(self):
        """ Initializes the NewUserDialog and its UI."""
        super().__init__(ui_path=os_util.get_resource_path(r'resources\ui\new_user_dialog.ui'))

class SetPathDialog(GLMDialog):

    def __init__(self, software : str, path : str=''):
        """ Initializes the SetPathDialog and its UI."""
        super().__init__(ui_path=os_util.get_resource_path(r'resources\ui\set_path_dialog.ui'))

        # Label setup
        self.software_folder_path_label.setText(f'{software} Folder Path')

        # Line edit setup
        self.path_line_edit.setText(path)

        # Folder button setup
        self.folder_button.clicked.connect(self._on_folder_button_clicked)

    def _on_folder_button_clicked(self):
        """ Called when the folder button is clicked."""

        folder = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Folder")
        self.path_line_edit.setText(folder)