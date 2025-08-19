from maya import cmds

def create_fk_long_controls():
    selection = cmds.ls(sl=True)
    controller = None
    preParent = None
    for i in selection:
        cmds.select(cl=True)
        if controller == None or cmds.objExists(controller) == False:
            controller1 = cmds.circle(nr=(1, 0, 0), name=i + "_ctrl")[0]
        else:
            controller1 = cmds.duplicate(controller, name=i + "_ctrl")[0]

        grp = cmds.group(em=1, name=i + "_ctrl_grp")
        cmds.parent(controller1, grp)
        pc = cmds.parentConstraint(i, grp, mo=0)
        cmds.delete(pc)
        cmds.pointConstraint(controller1, i, mo=0)
        cmds.orientConstraint(controller1, i, mo=0)
        if preParent != None:
            cmds.parent(grp, preParent)
        preParent = controller1