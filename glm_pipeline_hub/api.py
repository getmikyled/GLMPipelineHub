# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import os
import subprocess

from glm.core.users import users_utility as users_util

__all__ = [
            'MACHINE_ID', 'launch_maya', 'launch_blender', 'launch_substance_painter', 'launch_nuke',     # Launch
        ]

MACHINE_ID = users_util.get_machine_id()
PYTHON_PATH = r'G:\Shared drives\GLM\06_PIPELINE\python\source'
MAYA_SCRIPTS_PATH = os.path.join(PYTHON_PATH, r'glm\maya')

# -------------------------------------------
# App Launcher API

def launch_maya(file=None):
    """ Launches Maya.

    Args:
        file (str): The file to open Maya in.
    """

    user_info = users_util.get_users()[MACHINE_ID]
    maya_path = user_info[users_util.MAYA_USER_ATTR]
    maya_app_dir = user_info[users_util.LOCAL_MAYA_USER_ATTR]

    maya_exe_path = os.path.join(maya_path, r'bin\maya.exe')
    maya_args = [maya_exe_path]

    if file:
        maya_args.append(file)

    # Inherit current environment and add necessary paths
    env = os.environ.copy()
    env['MAYA_APP_DIR'] = maya_app_dir
    env['PYTHONPATH'] = PYTHON_PATH + os.pathsep + MAYA_SCRIPTS_PATH

    # Remove QT from environment so that it does not interfere with Maya's QT Plugin
    for key in list(env):
        if key.startswith("QT_") or key.startswith("PYSIDE") or key.startswith("PYQT"):
            env.pop(key)

    subprocess.Popen(maya_args, env=env, close_fds=True,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)

def launch_blender(file : str=None):
    """ Launches Blender.

    Args:
        file (str): The file to open Blender in. # TO DO: MUST BE IMPLEMENTED.
    """

    blender_path = os.path.join(users_util.get_users()[MACHINE_ID][users_util.BLENDER_USER_ATTR], 'blender.exe')

    blender_args = [blender_path, '--app-template', 'Guardians_Lament']

    subprocess.Popen(blender_args)

def launch_substance_painter(file=None):
    """ Launches Nuke.

    Args:
        file (str): The file to open Nuke in. # TO DO: MUST BE IMPLEMENTED.
    """

    user_info = users_util.get_users()[MACHINE_ID]
    substance_painter_path = os.path.join(user_info[users_util.SUBSTANCE_PAINTER_USER_ATTR], 'Adobe Substance 3D Painter.exe')

    substance_painter_args = [substance_painter_path]

    subprocess.Popen(substance_painter_args)

def launch_nuke(file=None):
    """ Launches Nuke.

    Args:
        file (str): The file to open Nuke in. # TO DO: MUST BE IMPLEMENTED.
    """
    nuke_path = users_util.get_users()[MACHINE_ID][users_util.NUKE_USER_ATTR]

# -------------------------------------------
# Shot Manager API


# -------------------------------------------
# System Profile API