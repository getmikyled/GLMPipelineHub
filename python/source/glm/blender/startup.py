# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import bpy
import addon_utils
import sys
import os

PYTHON_PATH = r"G:\Shared drives\GLM\06_PIPELINE\python\source"
if PYTHON_PATH not in sys.path:
    sys.path.append(PYTHON_PATH)

def _enable_system_add_ons():
    """Enable system add-ons"""
    print('bruh')
    for mod in addon_utils.modules():
        # If they begin with the system prefix, add it
        if mod.__name__.startswith('bl_ext.system'):
            print(f'enabled {mod.__name__}')
            addon_utils.enable(mod.__name__)

def _disable_system_add_ons():
    """Disable system add-ons"""
    for mod in addon_utils.modules():
        # If they begin with the system prefix, add it
        if mod.__name__.startswith('bl_ext.system'):
            print(f'disabled {mod.__name__}')
            addon_utils.enable(mod.__name__)
print('man')
bpy.app.handlers.load_post.append(_enable_system_add_ons)