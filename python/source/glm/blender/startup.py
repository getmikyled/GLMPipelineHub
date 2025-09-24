# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import bpy
import addon_utils

GLM_MODULES = {
    'bl_ext.system.photographer',
    'bl_ext.system.render_preset',
    'bl_ext.system.eevee_projectors',
    'bl_ext.system.substance_textures_importer',
    'bl_ext.system.you_are_autosave'
}

@bpy.app.handlers.persistent
def enable_glm_addons(arg1 = None, arg2 = None):
    """Enable system add-ons"""
    for module in addon_utils.modules():
        if module.__name__ in GLM_MODULES:
            print(f'enabled {module.__name__}')
            bpy.ops.preferences.addon_enable(module=module.__name__)