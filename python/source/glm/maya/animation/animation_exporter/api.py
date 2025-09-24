# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import os
import tempfile
import shutil

import glm.maya.maya_contexts as maya_contexts
from glm.blender.background.api import create_animation_cache_blend_file

import maya.mel as mel

import maya.cmds as cmds

TEMP_EXPORT_NAME = 'temp_glm_animation_export'
TEMP_DIR = os.path.join(tempfile.gettempdir(), TEMP_EXPORT_NAME).replace('\\','/')
TEMP_CACHE_PATH = os.path.join(TEMP_DIR, f'{TEMP_EXPORT_NAME}.xml').replace('\\','/')

def export_animation_to_blender(deforming_geometry: list[str], start_frame: int, end_frame: int,
                                model_paths: {str: str}, usd_path: str, blend_path: str):

    # Delete temp directory if it exists, and create it
    if os.path.exists(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.makedirs(TEMP_DIR)

    # ------------------------------------------------------------------------------------------------
    # Save current Maya file
    cmds.file(save=True, force=True)

    # Bake to geo cache
    with maya_contexts.restore_selection():
        # Delete any existing geometry caches
        delete_geometry_caches()

        # Select deforming geometry
        cmds.select(deforming_geometry)

        # Cache deforming geometry
        create_geometry_cache(TEMP_DIR, TEMP_EXPORT_NAME, start_frame, end_frame)

    # ------------------------------------------------------------------------------------------------
    # Create toUSD scene
    # Note: Discards cache changes in base scene to keep animation scene clean
    cmds.file(newFile=True, force=True)

    # Import your model and select geometry
    for namespace, model_path in model_paths.items():
        cmds.file(model_path, i=True, namespace=namespace)

    # Import geo cache
    deforming_geo_shapes = []
    for transform in deforming_geometry:
        shapes = cmds.listRelatives(transform, shapes=True)
        deforming_geo_shapes.append(shapes[0])
    for geo in deforming_geo_shapes:
        # Attach the cache (Maya creates a cacheFile node and connects it to a history switch)
        cache_path = os.path.join(TEMP_DIR, TEMP_CACHE_PATH)
        switch = mel.eval(f'createHistorySwitch("{geo}",false)')
        cmds.cacheFile(f=cache_path, cnm=geo, ia=f'{switch}.inp[0]', attachFile=True)
        cmds.setAttr(f'{switch}.playFromCache', 1)

    # ------------------------------------------------------------------------------------------------
    # Export all as USD
    export_all_as_usd(export_path=usd_path, start_frame=start_frame, end_frame=end_frame)

    # ------------------------------------------------------------------------------------------------
    # Import in blender
    create_animation_cache_blend_file(blend_path=blend_path, import_path=usd_path)

    print('Animation export is now complete.')

def find_obj_with_name(str):
    objs = cmds.ls()
    for obj in objs:
        if str in obj:
            return obj

def select_deforming_geometry():
    # Find the root object of the geometry, characterized by 'modelMain'
    root = find_obj_with_name('modelMain')

    # Get set of deforming geometry
    deforming_geo = set()
    descendents = cmds.listRelatives(root, allDescendents=True, fullPath=True) or []
    for descendent in descendents:
        # Check if node is of type 'mesh'
        if cmds.nodeType(descendent) == 'mesh':
            parent = cmds.listRelatives(descendent, parent=True, fullPath=True)
            if parent[0] not in deforming_geo:
                deforming_geo.add(parent[0])

    cmds.select(list(deforming_geo))


def create_geometry_cache(cache_dir : str, cache_name : str, start_frame: int, end_frame: int):
    """Create a geometry cache at the specified directory, name, and time range."""
    mel.eval(f'doCreateGeometryCache 6 {{ "3", {str(start_frame)}, {str(end_frame)}, "OneFilePerFrame", "1", "{cache_dir}","0", "{cache_name}","0", "add", "0", "1", "1","0","1","mcx","0" }} ;')

def delete_geometry_caches():
    """Delete any geometry cache nodes left over in the Maya scene.

    Without cleanup, the scene becomes super laggy.
    """
    # Query cache file nodes
    cache_nodes = cmds.ls(type='cacheFile')
    if not cache_nodes:
        print("No cacheFile nodes found.")
        return

    for node in cache_nodes:
        print(f"Deleting cache node: {node}")
        connections = cmds.listConnections(node, s=False, d=True, plugs=True) or []
        for conn in connections:
            try:
                cmds.disconnectAttr(f"{node}.outCacheData", conn)
            except:
                pass
        cmds.delete(node)

def export_all_as_usd(export_path, start_frame: int, end_frame: int):
    cmds.file(export_path,
    force = True,
    options = f';exportUVs=1;exportSkels=none;exportSkin=none;exportBlendShapes=0;exportDisplayColor=0;;exportColorSets=1;exportComponentTags=1;defaultMeshScheme=catmullClark;animation=1;eulerFilter=0;staticSingleSample=0;startTime={start_frame};endTime={end_frame};frameStride=1;frameSample=0.0;defaultUSDFormat=usda;parentScope=;shadingMode=useRegistry;convertMaterialsTo=[UsdPreviewSurface];exportRelativeTextures=automatic;exportInstances=1;exportVisibility=1;mergeTransformAndShape=1;stripNamespaces=0;worldspace=0',
    type = 'USD Export',
    preserveReferences = True,
    exportAll = True)