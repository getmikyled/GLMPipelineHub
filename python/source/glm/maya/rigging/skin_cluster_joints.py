import maya.cmds as cmds
import maya.api.OpenMaya as om

def get_average_position(verts):
    """Returns average world position of selected vertices."""
    points = [cmds.pointPosition(v, world=True) for v in verts]
    if not points:
        return None
    avg = [sum(coord) / len(points) for coord in zip(*points)]
    return avg

def create_joint_at_position(pos):
    """Creates a joint at given world position."""
    joint = cmds.joint(position=pos, name='placed_joint#')
    cmds.select(clear=True)
    return joint

def apply_skin_cluster_joint():
    sel = cmds.ls(selection=True, flatten=True)
    if not sel:
        cmds.error("Please select a mesh or some vertices.")

    verts = [v for v in sel if ".vtx" in v]
    obj = sel[0].split('.')[0]

    # If no vertex selected, use all vertices of the object
    if not verts:
        verts = cmds.ls(f'{obj}.vtx[*]', flatten=True)

    avg_pos = get_average_position(verts)
    if not avg_pos:
        cmds.error("Could not calculate average position.")

    # Check for existing skinCluster
    history = cmds.listHistory(obj)
    existing_skin = cmds.ls(history, type='skinCluster') if history else []

    skin = None
    created_temp_skin = False

    if not existing_skin:
        # Create a temporary joint and skinCluster
        temp_joint = cmds.joint(name='temp_joint#')
        skin = cmds.skinCluster(temp_joint, obj, toSelectedBones=True)[0]
        created_temp_skin = True
        cmds.delete(temp_joint)
    else:
        skin = existing_skin[0]

    # Create final joint
    joint = create_joint_at_position(avg_pos)
    print(f"Joint created at: {avg_pos}")

    # Delete the temporary skinCluster if we made it
    if created_temp_skin and cmds.objExists(skin):
        cmds.delete(skin)
        print(f"Deleted temporary skinCluster: {skin}")
    else:
        print("No temporary skinCluster was created; original skin left untouched.")
