# Copyright - Guardian's Lament 2025

import os
import subprocess

from glm_pipeline_hub.users import users_utility as users_util

__all__ = [
            'launch_maya', 'launch_blender', 'launch_nuke',     # Launch
            'get_shots', 'DEPARTMENTS',
            ]

_MACHINE_ID = users_util.get_machine_id()
_USERS = users_util.get_users()
if _MACHINE_ID in _USERS.keys():
    _USER_INFO = users_util.get_users()[_MACHINE_ID]
    _MAYA_PATH = _USER_INFO['maya_path']
    _MAYA_APP_DIR = os.path.expanduser(r'~\Documents\maya')
    _BLENDER_PATH = _USER_INFO['blender_path']
    _NUKE_PATH = _USER_INFO['nuke_path']
    _PYTHON_PATH = r'G:\Shared drives\GLM\06_PIPELINE\python'

DEPARTMENTS = ['PREVIS_LAYOUT', 'ANIM', 'FINAL_LAYOUT', 'LIGHT', 'FX_CFX', 'COMP']

# -------------------------------------------
# App Launcher API

def launch_maya(file=None):
    """ Launches Maya.

        Args:
            file (str): The file to open Maya in.
        """

    maya_exe_path = os.path.join(_MAYA_PATH, r'bin\maya.exe')
    maya_args = [maya_exe_path]

    if file:
        maya_args.append(file)

    # Inherit current environment and add necessary paths
    env = os.environ.copy()
    env['MAYA_APP_DIR'] = _MAYA_APP_DIR
    env['PYTHONPATH'] = _PYTHON_PATH

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

    blender_path = r'G:\Shared drives\GLM\06_PIPELINE\Blender\blender.exe'
    blender_args = [blender_path, '--app-template', 'Guardians_Lament']

    subprocess.Popen(blender_args)

def launch_nuke(file=None):
    """ Launches Nuke.

        Args:
            file (str): The file to open Nuke in. # TO DO: MUST BE IMPLEMENTED.
        """
    pass

# -------------------------------------------
# Shot Manager API

def get_shots():
    SHOT_PATH = 'G:/Shared drives/GLM/03_SHOTS'
    black_list = ['TEMPLATE']

    return [dir for dir in os.listdir(SHOT_PATH) if (os.path.isdir(f'{SHOT_PATH}/{dir}') and dir not in black_list)]

# -------------------------------------------
# System Profile API