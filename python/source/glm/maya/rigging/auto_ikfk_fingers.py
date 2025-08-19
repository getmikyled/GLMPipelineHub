import maya.cmds as cmds
import maya.api.OpenMaya as om2
import re

def duplicate_joint_chain(root_joint, suffix):
    new_chain = cmds.duplicate(root_joint, renameChildren=True)
    renamed_chain = []
    for jnt in new_chain:
        base = jnt.replace('_anim_jnt', '')
        new_name = f'{base}_{suffix}_jnt'
        jnt = cmds.rename(jnt, new_name)
        renamed_chain.append(jnt)
    return renamed_chain

def create_fk_controls(joint_chain, fk_template_curve=None):
    controls = []
    groups = []
    for jnt in joint_chain:
        ctrl_name = jnt.replace('_fk_jnt', '_fk_ctrl')
        if fk_template_curve and cmds.objExists(fk_template_curve):
            ctrl = cmds.duplicate(fk_template_curve, name=ctrl_name)[0]
        else:
            ctrl = cmds.circle(name=ctrl_name, normal=[1, 0, 0], radius=0.5)[0]
        grp = cmds.group(ctrl, name=ctrl + '_grp')
        cmds.delete(cmds.parentConstraint(jnt, grp))
        cmds.pointConstraint(ctrl, jnt)
        cmds.orientConstraint(ctrl, jnt)
        controls.append(ctrl)
        groups.append(grp)
    for i in range(1, len(groups)):
        cmds.parent(groups[i], controls[i - 1])
    return controls, groups

def create_ik_controls(ik_chain, ik_template_curve=None):
    start_jnt = ik_chain[0]
    end_jnt = ik_chain[-1]
    ik_handle, eff = cmds.ikHandle(startJoint=start_jnt, endEffector=end_jnt, solver='ikRPsolver')
    ik_ctrl_name = end_jnt.replace('_ik_jnt', '_ik_ctrl')
    if ik_template_curve and cmds.objExists(ik_template_curve):
        ik_ctrl = cmds.duplicate(ik_template_curve, name=ik_ctrl_name)[0]
    else:
        ik_ctrl = cmds.circle(name=ik_ctrl_name, normal=[1, 0, 0], radius=0.5)[0]
    ik_grp = cmds.group(ik_ctrl, name=ik_ctrl + '_grp')
    cmds.delete(cmds.parentConstraint(end_jnt, ik_grp))
    cmds.parent(ik_handle, ik_ctrl)
    return ik_ctrl, ik_grp, ik_handle

def calculate_pv_position(top, mid, end):
    top_pos = cmds.xform(top, query=True, worldSpace=True, translation=True)
    mid_pos = cmds.xform(mid, query=True, worldSpace=True, translation=True)
    end_pos = cmds.xform(end, query=True, worldSpace=True, translation=True)

    top_v = om2.MVector(*top_pos)
    mid_v = om2.MVector(*mid_pos)
    end_v = om2.MVector(*end_pos)

    line = end_v - top_v
    point = mid_v - top_v
    scale_value = (line * point) / (line * line)
    projected = line * scale_value + top_v

    root_to_mid = (mid_v - top_v).length()
    mid_to_end = (end_v - mid_v).length()
    total_len = root_to_mid + mid_to_end

    direction = (mid_v - projected).normal() * total_len
    return (mid_v + direction)

def create_pole_vector(ik_chain, ik_handle, base_name_full):
    top, mid, end = ik_chain[0], ik_chain[1], ik_chain[2]
    pv_pos = calculate_pv_position(top, mid, end)
    pv_name = base_name_full + '_PV_ctrl'
    pole_vector_ctrl = cmds.spaceLocator(name=pv_name)[0]
    cmds.setAttr(pole_vector_ctrl + '.localScaleX', 0.3)
    cmds.setAttr(pole_vector_ctrl + '.localScaleY', 0.3)
    cmds.setAttr(pole_vector_ctrl + '.localScaleZ', 0.3)
    pv_grp = cmds.group(pole_vector_ctrl, name=pv_name + '_grp')
    cmds.xform(pv_grp, worldSpace=True, translation=(pv_pos.x, pv_pos.y, pv_pos.z))
    cmds.poleVectorConstraint(pole_vector_ctrl, ik_handle)
    return pole_vector_ctrl, pv_grp

def build_multi_fk_ik_rig(fk_template_curve=None, ik_template_curve=None):
    selection = cmds.ls(selection=True, type='transform')

    if not selection or len(selection) < 2:
        cmds.error("Select one or more _anim_jnt root joints, then the IK/FK switch controller LAST.")

    switch_ctrl = selection[-1]
    joint_selection = selection[:-1]
    joint_selection = [j for j in joint_selection if j.endswith('_anim_jnt') and cmds.nodeType(j) == 'joint']

    anim_roots = []
    for jnt in joint_selection:
        parent = cmds.listRelatives(jnt, parent=True, type='joint')
        if not parent:
            anim_roots.append(jnt)
        elif parent[0] not in joint_selection:
            anim_roots.append(jnt)

    if not anim_roots:
        cmds.error("No valid root joints found. Make sure your joints end in '_anim_jnt'.")

    # Auto-detect shared prefix (everything before _Claw_#, e.g., Lf_Claw)
    match = re.match(r'(.*?_Toe)_\d+_\d+_anim_jnt', anim_roots[0])
    prefix = match.group(1) if match else 'Toe'

    all_jnt_grp = f'{prefix}_jnt_grp'
    all_ctrl_grp = f'{prefix}_ctrl_grp'

    if not cmds.objExists(all_jnt_grp):
        all_jnt_grp = cmds.group(empty=True, name=all_jnt_grp)
    if not cmds.objExists(all_ctrl_grp):
        all_ctrl_grp = cmds.group(empty=True, name=all_ctrl_grp)

    for root in anim_roots:
        base_name_full = root.replace('_anim_jnt', '')

        jnt_grp_name = base_name_full + '_jnt_grp'
        ctrl_grp_name = base_name_full + '_ctrl_grp'

        jnt_grp = cmds.group(empty=True, name=jnt_grp_name, parent=all_jnt_grp)
        ctrl_grp = cmds.group(empty=True, name=ctrl_grp_name, parent=all_ctrl_grp)

        fk_joints_grp = cmds.group(empty=True, name=base_name_full + '_fk_jnt_grp', parent=jnt_grp)
        ik_joints_grp = cmds.group(empty=True, name=base_name_full + '_ik_jnt_grp', parent=jnt_grp)
        fk_controls_grp = cmds.group(empty=True, name=base_name_full + '_fk_ctrl_grp', parent=ctrl_grp)
        ik_controls_grp = cmds.group(empty=True, name=base_name_full + '_ik_ctrl_grp', parent=ctrl_grp)
        pv_controls_grp = cmds.group(empty=True, name=base_name_full + '_pv_ctrl_grp', parent=ctrl_grp)

        attr_name = f'{base_name_full}_fkIkSwitch'

        fk_chain = duplicate_joint_chain(root, 'fk')
        ik_chain = duplicate_joint_chain(root, 'ik')

        fk_ctrls, fk_grps = create_fk_controls(fk_chain, fk_template_curve=fk_template_curve)
        cmds.parent(fk_chain[0], fk_joints_grp)
        cmds.parent(ik_chain[0], ik_joints_grp)
        cmds.parent(fk_grps[0], fk_controls_grp)

        ik_ctrl, ik_grp, ik_handle = create_ik_controls(ik_chain, ik_template_curve=ik_template_curve)
        cmds.parent(ik_grp, ik_controls_grp)

        pv_ctrl, pv_grp = create_pole_vector(ik_chain, ik_handle, base_name_full)
        cmds.parent(pv_grp, pv_controls_grp)

        anim_chain = cmds.listRelatives(root, allDescendents=True, type='joint') or []
        anim_chain = [root] + list(reversed(anim_chain))

        for anim_jnt, fk_jnt, ik_jnt in zip(anim_chain, fk_chain, ik_chain):
            constraint = cmds.parentConstraint(fk_jnt, ik_jnt, anim_jnt, maintainOffset=True)[0]
            targets = cmds.parentConstraint(constraint, query=True, targetList=True)
            if not cmds.attributeQuery(attr_name, node=switch_ctrl, exists=True):
                cmds.addAttr(switch_ctrl, longName=attr_name, attributeType='enum', enumName='fk:ik', keyable=True)
            cmds.setAttr(f'{constraint}.{targets[0]}W0', 1)
            cmds.setAttr(f'{constraint}.{targets[1]}W1', 0)
            cmds.connectAttr(f'{switch_ctrl}.{attr_name}', f'{constraint}.{targets[1]}W1', force=True)

            rev_node = cmds.shadingNode('reverse', asUtility=True, name=f'{base_name_full}_fkVis_reverse')
            cmds.connectAttr(f'{switch_ctrl}.{attr_name}', f'{rev_node}.inputX')
            cmds.connectAttr(f'{rev_node}.outputX', f'{constraint}.{targets[0]}W0')

        fk_grp_top = fk_grps[0]
        cmds.connectAttr(f'{rev_node}.outputX', f'{fk_grp_top}.visibility', force=True)
        cmds.connectAttr(f'{switch_ctrl}.{attr_name}', f'{ik_grp}.visibility', force=True)
        cmds.connectAttr(f'{switch_ctrl}.{attr_name}', f'{pv_grp}.visibility', force=True)

def create_ikfk_fingers():
    build_multi_fk_ik_rig(fk_template_curve='curve1', ik_template_curve='curve2')



