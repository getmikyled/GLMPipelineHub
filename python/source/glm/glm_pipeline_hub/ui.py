# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import os

from PyQt5 import QtWidgets, uic, QtGui

import glm.core.users.users_utils as users_util

import styles
import api

import sitecustomize

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
            os.path.join(os.path.dirname(__file__), 'main_window.ui'),
            baseinstance=self
        )

        self._init_user()
        self._init_ui()

        self.show()

    def _init_ui(self):
        """ Initialize the window's UI."""

        # Set widget
        self.setWindowIcon(QtGui.QIcon(os.path.join(sitecustomize.IMAGES_DIR, 'glm_icon.jpg')))

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
        self.maya_launcher_button.setIcon(QtGui.QIcon(
            os.path.join(sitecustomize.IMAGES_DIR, 'glm_pipeline_hub', 'app_icons', 'maya.png')))
        self.maya_launcher_button.clicked.connect(api.launch_maya)
        self.blender_launcher_button.clicked.connect(api.launch_blender)
        self.blender_launcher_button.setIcon(QtGui.QIcon(
            os.path.join(sitecustomize.IMAGES_DIR, 'glm_pipeline_hub', 'app_icons', 'blender.png')))
        self.substance_painter_launcher_button.clicked.connect(api.launch_substance_painter)
        self.substance_painter_launcher_button.setIcon(QtGui.QIcon(
            os.path.join(sitecustomize.IMAGES_DIR, 'glm_pipeline_hub', 'app_icons', 'substance_painter.png')))

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

        # Machine ID setup
        machine_id = users_util.get_machine_id()
        self.user_machine_id_label.setText(machine_id)

        user_info = users_util.get_users()[machine_id]

        # Username setup
        self.username_label.setText(user_info['username'])
        self.edit_username_button.clicked.connect(self._edit_username)

        # Maya directory setup
        self.maya_directory_label.setText(user_info[users_util.MAYA_USER_ATTR])
        self.edit_maya_directory_button.clicked.connect(
            lambda: self._input_new_path('Maya', users_util.MAYA_USER_ATTR, self.maya_directory_label))

        # Local Maya directory setup
        self.local_maya_directory_label.setText(user_info[users_util.LOCAL_MAYA_USER_ATTR])
        self.edit_local_maya_directory_button.clicked.connect(
            lambda: self._input_new_path('Local Maya', users_util.LOCAL_MAYA_USER_ATTR,
                                         self.local_maya_directory_label))

        # Blender directory setup
        self.blender_directory_label.setText(user_info[users_util.BLENDER_USER_ATTR])
        self.edit_blender_directory_button.clicked.connect(
            lambda: self._input_new_path('Blender', users_util.BLENDER_USER_ATTR, self.blender_directory_label)
        )

        # Substance Painter directory setup
        self.substance_painter_directory_label.setText(user_info[users_util.SUBSTANCE_PAINTER_USER_ATTR])
        self.edit_substance_painter_directory_button.clicked.connect(
            lambda: self._input_new_path('Substance Painter', users_util.SUBSTANCE_PAINTER_USER_ATTR,
                                 self.substance_painter_directory_label))

        # Local Substance Painter directory setup
        self.local_substance_painter_directory_label.setText(user_info[users_util.LOCAL_SUBSTANCE_PAINTER_USER_ATTR])
        self.edit_local_substance_painter_directory_button.clicked.connect(
            lambda: self._input_new_path('Local Substance Painter',
                                         users_util.LOCAL_SUBSTANCE_PAINTER_USER_ATTR,
                                         self.local_substance_painter_directory_label))

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

        if users_util.MAYA_USER_ATTR not in users_util.get_users()[api.MACHINE_ID].keys():
            maya_path = r'C:\Program Files\Autodesk\Maya2024'
            if os.path.exists(maya_path):
                users_util.set_user_attr(self.machine_id, users_util.MAYA_USER_ATTR, maya_path)
            else:
                self._input_new_path('Maya', users_util.MAYA_USER_ATTR)

        if users_util.LOCAL_MAYA_USER_ATTR not in users_util.get_users()[api.MACHINE_ID].keys():
            local_maya_path = os.path.expanduser(r'~\Documents\maya')
            if os.path.exists(local_maya_path):
                users_util.set_user_attr(self.machine_id, users_util.LOCAL_MAYA_USER_ATTR, local_maya_path)
            else:
                self._input_new_path('Local Maya', users_util.LOCAL_MAYA_USER_ATTR)

        if users_util.BLENDER_USER_ATTR not in users_util.get_users()[api.MACHINE_ID].keys():
            blender_path = r'G:\Shared drives\GLM\06_PIPELINE\Blender'
            if os.path.exists(blender_path):
                users_util.set_user_attr(self.machine_id, users_util.BLENDER_USER_ATTR, blender_path)
            else:
                self._input_new_path('Blender', users_util.BLENDER_USER_ATTR)

        if users_util.SUBSTANCE_PAINTER_USER_ATTR not in users_util.get_users()[api.MACHINE_ID].keys():
            substance_painter_path = r'C:\Program Files\Adobe\Adobe Substance 3D Painter'
            if os.path.exists(substance_painter_path) :
                users_util.set_user_attr(self.machine_id, users_util.SUBSTANCE_PAINTER_USER_ATTR,
                                         substance_painter_path)
            else:
                self._input_new_path('Substance Painter', users_util.SUBSTANCE_PAINTER_USER_ATTR)

        if users_util.LOCAL_SUBSTANCE_PAINTER_USER_ATTR not in users_util.get_users()[api.MACHINE_ID].keys():
            local_substance_painter_path = os.path.expanduser(r'~\Documents\Adobe\Adobe Substance 3D Painter')
            if os.path.exists(local_substance_painter_path):
                users_util.set_user_attr(self.machine_id, users_util.LOCAL_SUBSTANCE_PAINTER_USER_ATTR,
                                         local_substance_painter_path)
            else:
                self._input_new_path('Local Substance Painter', users_util.LOCAL_SUBSTANCE_PAINTER_USER_ATTR)

    def _get_shots(self) -> list[str]:
        """ Get a list of all the shots in the shots directory.

        Excludes blacklisted shots.

        Returns:
            list[str]: A list of all the shots in the shots directory.
        """

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
                return self._input_new_username(True)
        return ''

    def _edit_username(self):
        username = self._input_new_username(force=False)

        if username:
            users_util.set_user_attr(self.machine_id, 'username', username)
            self.username_line_edit.setText(username)

    def _input_new_path(self, software: str, attr: str, label: QtWidgets.QLabel = None) -> str:
        """ Prompt the user to input a new path.

        Args:
            software (str): The name of the software that the user is being prompted a path for.
            default (str): The default path to set the dialog to, and to return if user cancelled or ignored.

        Returns:
            str: The new path that the user inputted. Returns default if nothing was inputted.
        """

        default_dir = users_util.get_users()[users_util.get_machine_id()].get(attr, '')

        dialog = SetPathDialog(software=software, path=default_dir)
        result = dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            new_dir = dialog.path_line_edit.text()
        else:
            new_dir = default_dir

        # Update new path for user
        users_util.set_user_attr(users_util.get_machine_id(), attr, new_dir)
        if label:
            label.setText(new_dir)

        return new_dir


class NewUserDialog(QtWidgets.QDialog):

    def __init__(self):
        """ Initializes the NewUserDialog and its UI."""
        super().__init__()

        uic.loadUi(
            os.path.join(os.path.dirname(__file__), 'new_user_dialog.ui'),
            baseinstance=self
        )

        self.setStyleSheet(styles.STYLESHEET)

        self.show()

class SetPathDialog(QtWidgets.QDialog):

    def __init__(self, software : str, path : str):
        """ Initializes the SetPathDialog and its UI.

        Args:
            software (str): The name of the software that the user is being prompted a path for.
            path (str): The default path to set the dialog to.
        """
        super().__init__()

        uic.loadUi(
            os.path.join(os.path.dirname(__file__), 'set_path_dialog.ui'),
            baseinstance=self
        )

        self.setStyleSheet(styles.STYLESHEET)

        # Label setup
        self.software_folder_path_label.setText(f'{software} Folder Path')

        # Line edit setup
        self.path_line_edit.setText(path)

        # Folder button setup
        self.folder_button.clicked.connect(self._on_folder_button_clicked)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.button(QtWidgets.QDialogButtonBox.Ignore).clicked.connect(self.reject)

        self.show()

    def _on_folder_button_clicked(self):
        """ Called when the folder button is clicked."""

        folder = os.path.normpath(QtWidgets.QFileDialog.getExistingDirectory(None, "Select Folder"))
        self.path_line_edit.setText(folder)