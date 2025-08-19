# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import os

import maya.cmds as cmds

import glm.maya.animation.animation_exporter.api as api
import glm.core.os.path as glm_path
import glm.core.qt.ui_loader as ui_loader
from glm.core.qt.singleton_main_window import SingletonMayaMainWindow

from PySide2 import QtGui, QtWidgets

import sitecustomize

FOLDER_IMAGE_PATH = os.path.join(sitecustomize.IMAGES_DIR, r'images\common\folder.png')

class AnimationExporterMainWindow(SingletonMayaMainWindow):

    def __init__(self):
        """Initialize Animation Exporter Main Window."""
        super().__init__()
        # Load UI
        ui_loader.load_ui(
            os.path.join(os.path.abspath(os.path.dirname(__file__)), 'main_window.ui'),
            self
        )

        # -------------------------------------------------------------------------------------
        # Blender output path setup

        # Get current scene path
        scene_path = cmds.file(query=True, sceneName=True)
        if not scene_path:
            raise Exception('Scene must be saved to a path in order to use animation exporter.')
        scene_path = os.path.normpath(scene_path)

        # Check if Maya directory ('01_MAYA') exists
        maya_directory = glm_path.search_parents_for_directory_recursive(scene_path, '01_MAYA')
        if maya_directory:
            blender_output_path = os.path.join(
                os.path.dirname(glm_path.search_parents_for_directory_recursive(scene_path, '01_MAYA')),
                '02_BLENDER')
        else:
            blender_output_path = sitecustomize.REPOSITORY_DIR

        blender_output_name = os.path.basename(scene_path).split('.')[0].replace('base', 'blender')
        blender_output_path = os.path.join(blender_output_path, f'{blender_output_name}.blend')
        self.blender_output_path_line_edit.setText(blender_output_path)

        # Set up folder button
        self.folder_button.setIcon(QtGui.QIcon(r':\folderPlacholder.png'))
        self.folder_button.clicked.connect(self._set_blend_output_path)

        # -------------------------------------------------------------------------------------
        # Time Range of Animation

        # Set up apply scene frame range button
        self.apply_scene_frame_range_button.clicked.connect(self._apply_scene_frame_range)

        # Set up start frame and end frame
        int_validator = QtGui.QIntValidator()
        self.start_frame_line_edit.setValidator(int_validator)
        self.end_frame_line_edit.setValidator(int_validator)
        self._apply_scene_frame_range()

        # -------------------------------------------------------------------------------------
        # Set up export button
        self.export_animation_to_blender_button.clicked.connect(self._on_export_animation_to_blender_button_clicked)

    def _set_blend_output_path(self):
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,  # parent (ok to pass your QWidget)
            "Select a File",  # title
            self.blender_output_path_line_edit.text(),  # starting directory
            "Blend Files (*.blend);;All Files (*)"  # filter
        )

        self.blender_output_path_line_edit.setText(os.path.normpath(file_path))

    def _apply_scene_frame_range(self):
        """Applies scene's frame range to start frame and end frame line edits."""
        self.start_frame_line_edit.setText(str(int(cmds.playbackOptions(query=True, minTime=True))))
        self.end_frame_line_edit.setText(str(int(cmds.playbackOptions(query=True, maxTime=True))))

    def _on_export_animation_to_blender_button_clicked(self):

        # Cache scene path for later
        scene_path = cmds.file(query=True, sceneName=True)

        # ------------------------------------------------------------------------------------------------
        # Import all references and fix naming of sets
        # If you don't remove reference part of object name, you won't be able to properly query the set
        refs = cmds.file(query=True, reference=True)
        for ref in refs:
            cmds.file(ref, importReference=True)

        sets = cmds.ls(type="objectSet")
        for set in sets:
            # Remove reference part of set name if it is not locked
            if len(cmds.ls(set, readOnly=True)) == 0:
                new_name = set.split(':')[-1]
                try:
                    cmds.rename(set, new_name)
                except:
                    pass
                    # Node is read only. Only way I could find to ignore read only nodes

        model_path = cmds.getAttr('RIG_INFO.modelPath')
        character_name = cmds.getAttr('RIG_INFO.characterName')
        deforming_geometry = cmds.sets('DEFORMING_GEO', query=True)

        # Export animation to blender
        api.export_animation_to_blender(deforming_geometry=deforming_geometry,
                                        start_frame=self.start_frame_line_edit.text(),
                                        end_frame=self.end_frame_line_edit.text(),
                                        character_name=character_name,
                                        model_path=model_path,
                                        blend_path=self.blender_output_path_line_edit.text()
                                        )

        # Open the original animation scene after done exporting
        cmds.file(scene_path, open=True, force=True)