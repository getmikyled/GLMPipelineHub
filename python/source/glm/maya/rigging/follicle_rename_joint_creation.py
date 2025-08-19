import maya.cmds as cmds

def rename_follicle_joints():
    nameBase = "Lf_Bk_Leg_Stretch_Ribbon"

    selection = cmds.ls(sl=True)
    for i in range(0, len(selection)):
        suffix = str(i + 1).zfill(2)

        FollicleName = nameBase + "_" + "follicle_" + suffix + ""
        cmds.rename(selection[i], FollicleName)
        cmds.select(cl=True)
        newJnt = cmds.joint(n=nameBase + "_" + suffix + "_jnt")

        cmds.parentConstraint(FollicleName, newJnt)