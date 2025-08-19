from maya import cmds

def create_groups_from_selection():
    selection = cmds.ls(sl=True, type='transform')

    for ctrl in selection:
        if not cmds.objExists(ctrl):
            continue

        # Get current parent (e.g., a control group or another control)
        parent = cmds.listRelatives(ctrl, parent=True)

        # Create the new group and snap it to the control
        grp_name = ctrl + "_180_grp"
        new_grp = cmds.group(empty=True, name=grp_name)
        cmds.delete(cmds.parentConstraint(ctrl, new_grp))  # Match transforms

        # Parent the control under the new group
        cmds.parent(ctrl, new_grp)

        # Restore the previous parent-child relationship
        if parent:
            cmds.parent(new_grp, parent[0])