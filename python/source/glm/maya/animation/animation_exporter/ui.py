# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import os
import re

import maya.cmds as cmds
from PySide6 import QtGui, QtWidgets, QtCore

import glm.maya.animation.animation_exporter.api as api
from glm.maya.animation.reference_rigs import api as reference_rigs
from glm.maya.rigging.rig_manager import api as rig_manager
import glm.core.os.path as glm_path
import glm.core.qt.ui_loader as ui_loader
from glm.core.qt.singleton_main_window import SingletonMayaMainWindow

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

        self.setFocusPolicy(QtCore.Qt.StrongFocus)

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
        # Setup rig list widget
        self._refresh_rig_list_widget()

        # -------------------------------------------------------------------------------------
        # Set up export button
        self.export_animation_to_blender_button.clicked.connect(self._on_export_animation_to_blender_button_clicked)

    def focusInEvent(self, event):
        super().focusInEvent(event)

        self._refresh_rig_list_widget()

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

    def _refresh_rig_list_widget(self):

        selected_items = [item.text() for item in self.rig_list_widget.selectedItems()]

        # Clear rig list widget
        self.rig_list_widget.clear()

        # Add items to rig list widget
        rig_references = reference_rigs.get_rig_reference_namespaces_without_prefix()
        self.rig_list_widget.addItems(rig_references)
        for i in range(self.rig_list_widget.count()):
            item = self.rig_list_widget.item(i)
            if item.text() in selected_items:
                item.setSelected(True)

    def _on_export_animation_to_blender_button_clicked(self):

        """"""
        # Cache scene path for later
        scene_path = cmds.file(query=True, sceneName=True)

        # Get selected rigs
        selected_rig_references = [item.text() for item in self.rig_list_widget.selectedItems()]
        if len(selected_rig_references) == 0:
            print('Warning: Must select at least one rig reference.')
            return

        rig_presets = rig_manager.get_rig_presets()

        # Get deforming geo and model path information for selected rigs
        total_deforming_geo = []
        model_paths = {}
        for rig_reference in selected_rig_references:
            # Remove any possible numbers added to rig reference namespace to query preset
            rig_preset_name = re.sub(r'\d+$', '', rig_reference)
            rig_preset = rig_presets[rig_preset_name]
            rig_reference_with_prefix = f'{reference_rigs.RIG_REFERENCE_PREFIX}{rig_reference}'

            # Get deforming geo
            deforming_geo = rig_preset[rig_manager.DEFORMING_GEO_KEY]
            total_deforming_geo.extend([f'{rig_reference_with_prefix}:{geo}' for geo in deforming_geo])

            # Get model paths
            model_paths[rig_reference_with_prefix] = rig_preset[rig_manager.MODEL_PATHS_KEY]

            # Set usd path
            base_name = os.path.basename(scene_path).split('.')[0].replace('base', 'usd')
            usd_path = os.path.join(
                os.path.dirname(glm_path.search_parents_for_directory_recursive(scene_path, '01_MAYA')),
                '02_BLENDER', f'{base_name}.usd')

        # Export animation to blender
        api.export_animation_to_blender(
            deforming_geometry=total_deforming_geo,
            start_frame=self.start_frame_line_edit.text(),
            end_frame=self.end_frame_line_edit.text(),
            model_paths=model_paths,
            usd_path=usd_path,
            blend_path=self.blender_output_path_line_edit.text()
        )

        # Open the original animation scene after done exporting
        cmds.file(scene_path, open=True, force=True)