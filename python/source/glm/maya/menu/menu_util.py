# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import maya.cmds as cmds

__all__ = [
    'create_glm_menu'
]

GLM_MENU_NAME = 'glmMenu'
ANIMATION_SUBMENU_NAME = 'Animation'
RIGGING_SUBMENU_NAME = 'Rigging'

#def my_menu_command(*args):
#    cmds.confirmDialog(title="Hello", message="You clicked the menu item!")

def create_glm_menu():
    # Check if it already exists to avoid duplicates
    if cmds.menu(GLM_MENU_NAME, exists=True):
        cmds.deleteUI(GLM_MENU_NAME, menu=True)

    # Add to Maya’s main menu bar
    cmds.menu(GLM_MENU_NAME, label='🎬GLM🎬', parent='MayaWindow', tearOff=True)
    animation_submenu = cmds.menuItem(label=ANIMATION_SUBMENU_NAME, subMenu=True, parent=GLM_MENU_NAME, tearOff=True)
    rigging_submenu = cmds.menuItem(label=RIGGING_SUBMENU_NAME, subMenu=True, parent=GLM_MENU_NAME, tearOff=True)

    # ------------------------------------------------------------------------------------------------------
    # Animation Submenu
    cmds.menuItem(label='Reference Rigs',
                  command='from glm.maya.animation.reference_rigs.ui' +
                          ' import ReferenceRigsMainWindow; ReferenceRigsMainWindow().show()',
                  parent=animation_submenu)
    cmds.menuItem(label='Animation Exporter',
                  command='from glm.maya.animation.animation_exporter.ui' +
                          ' import AnimationExporterMainWindow; AnimationExporterMainWindow().show()',
                  parent=animation_submenu)

    # ------------------------------------------------------------------------------------------------------
    # Rigging Submenu
    cmds.menuItem(label='Rig Manager',
                  command='from glm.maya.rigging.rig_manager.ui' +
                          ' import RigManagerMainWindow; RigManagerMainWindow().show()',
                  parent=rigging_submenu)
    cmds.menuItem(label='Curve Creator',
                  command= 'from curveCreator import curveUI; curveUI.showUI()',
                  parent=rigging_submenu)
    cmds.menuItem(divider=True)
    cmds.menuItem(label='FK Long Controls',
                  command='from glm.maya.rigging import fk_long_controls; fk_long_controls.create_fk_long_controls()',
                  parent=rigging_submenu)
    cmds.menuItem(label='Self Group Maker',
                  command='from glm.maya.rigging import self_group_maker; self_group_maker.create_groups_from_selection()',
                  parent=rigging_submenu)
    cmds.menuItem(label='Skin Cluster Joints',
                  command='from glm.maya.rigging import skin_cluster_joints; skin_cluster_joints.apply_skin_cluster_joint()',
                  parent=rigging_submenu)
    cmds.menuItem(label='Hide Local Axis',
                  command='from glm.maya.rigging import hide_local_axis; hide_local_axis.hide_local_axis()',
                  parent=rigging_submenu)
    cmds.menuItem(label='Auto IKFK Fingers',
                  command='from glm.maya.rigging import auto_ikfk_fingers; auto_ikfk_fingers.create_ikfk_fingers()',
                  parent=rigging_submenu)
    cmds.menuItem(label='Pole Vector Placement Finder',
                  command='from glm.maya.rigging import pole_vector_placement_finder; pole_vector_placement_finder.find_pole_vector_placement()',
                  parent=rigging_submenu)