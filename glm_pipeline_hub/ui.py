import os

from PyQt5 import QtWidgets, uic

from glm_pipeline_hub.core import get_resource_path
import glm_pipeline_hub.api as glm

__all__ = ['GLMPipelineHubMainWindow']

class GLMPipelineHubMainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()

        uic.loadUi(
            os.path.join(get_resource_path('resources\\ui\\main_window.ui')),
            baseinstance = self
        )

        self.show()

        # -------------------------------------------
        # Sidebar setup

        self.app_launcher_button.clicked.connect(lambda : self.stack.setCurrentIndex(0))
        self.shot_manager_button.clicked.connect(lambda : self.stack.setCurrentIndex(1))
        self.system_profile_button.clicked.connect(lambda : self.stack.setCurrentIndex(2))

        # -------------------------------------------
        # App Launcher Setup

        self.maya_launcher_button.clicked.connect(glm.launch_maya)
        self.blender_launcher_button.clicked.connect(glm.launch_blender)

        # -------------------------------------------
        # Shot manager setup

        # Shot setup
        self.shot_combo_box.addItems(glm.get_shots())

        # Department setup
        self.department_combo_box.addItems(glm.get_departments())

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