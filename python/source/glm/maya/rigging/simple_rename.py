import maya.cmds as cmds

nameBase = "Input"

selection = cmds.ls(sl = True)
for i in range(0, len(selection)):
    suffix = str(i + 1).zfill(2)
    
    FollicleName = "follicle_" + nameBase + "_" + suffix + ""
    cmds.rename(selection[i], FollicleName)