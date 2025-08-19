import maya.cmds as cmds

def hide_local_axis():
    # Get selected objects
    selection = cmds.ls(selection=True, long=True)

    if not selection:
        cmds.warning("No objects selected.")
    else:
        # Optionally include children (recursive)
        all_objects = []
        for obj in selection:
            all_objects.append(obj)
            all_objects += cmds.listRelatives(obj, allDescendents=True, fullPath=True) or []

        # Filter only transform nodes
        transforms = [obj for obj in all_objects if cmds.objectType(obj) == 'transform']

        # Hide local rotation axes
        for obj in transforms:
            if cmds.getAttr(obj + ".displayLocalAxis"):
                cmds.setAttr(obj + ".displayLocalAxis", False)

        print(f"Local rotation axes hidden for {len(transforms)} transform(s).")
