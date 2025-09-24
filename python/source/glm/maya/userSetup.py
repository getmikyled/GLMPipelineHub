# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import sys
import maya.utils

import menu

PYTHON_PATHS = [
    r'G:\Shared Drives\GLM\06_PIPELINE\python\source',
    r'G:\Shared Drives\GLM\06_PIPELINE\python\source\site-packages',
    r'G:\Shared Drives\GLM\06_PIPELINE\Blender\4.4\python\lib\site-packages'
]

# Initialize GLM menu
maya.utils.executeDeferred(menu.create_glm_menu)

for path in PYTHON_PATHS:
    sys.path.append(path)