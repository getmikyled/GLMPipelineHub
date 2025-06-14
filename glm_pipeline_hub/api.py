# Copyright - Guardian's Lament 2025

import os
import subprocess

__all__ = ['launch_maya', 'launch_blender', 'launch_nuke',
           'get_shots', 'get_departments']

DEPARTMENTS = ['PREVIS_LAYOUT', 'ANIM', 'FINAL_LAYOUT', 'LIGHT', 'FX_CFX', 'COMP']

# -------------------------------------------
# App Launcher API

def launch_maya(file=None):
    path = r'C:\Program Files\Autodesk\Maya2024\bin\maya.exe'
    maya_args = [path]

    if file:
        maya_args.append(file)

    # Inherit current environment and add necessary paths
    env = os.environ.copy()
    env['MAYA_APP_DIR'] = r'C:\Users\mikin\Documents\maya'
    env['PYTHONPATH'] = r'G:\Shared drives\GLM\06_PIPELINE\python'

    # Remove QT from environment so that it does not interfere with Maya's QT Plugin
    for key in list(env):
        if key.startswith("QT_") or key.startswith("PYSIDE") or key.startswith("PYQT"):
            env.pop(key)

    subprocess.Popen(maya_args, env=env, close_fds=True,
        creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)

def launch_blender(file=None):
    blender_path = r'G:\Shared drives\GLM\06_PIPELINE\Blender\blender.exe'
    blender_args = [blender_path, '--app-template', 'Guardians_Lament']

    subprocess.Popen(blender_args)

def launch_nuke(file=None):
    pass

# -------------------------------------------
# Shot Manager API

def get_shots():
    SHOT_PATH = 'G:/Shared drives/GLM/03_SHOTS'
    black_list = ['TEMPLATE']

    return [dir for dir in os.listdir(SHOT_PATH) if (os.path.isdir(f'{SHOT_PATH}/{dir}') and dir not in black_list)]

def get_departments():
    return DEPARTMENTS

# -------------------------------------------
# System Profile API