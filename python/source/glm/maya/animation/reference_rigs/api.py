import maya.cmds as cmds

RIG_REFERENCE_PREFIX = 'GLM_RIG_'

def add_rig_reference(file_path: str, namespace: str) -> str:
    reference_node = cmds.file(file_path,
                               reference=True,
                               namespace=f'{RIG_REFERENCE_PREFIX}{namespace}',
                               returnNewNodes=True)

    return reference_node

def get_rig_reference_namespaces() -> list[str]:
    references = cmds.ls(type='reference')

    reference_namespaces = [cmds.referenceQuery(reference, namespace=True, shortName=True)
                            for reference in references]

    return reference_namespaces

def get_rig_reference_namespaces_without_prefix() -> list[str]:
    reference_namespaces = get_rig_reference_namespaces()

    # Add reference to list if it has prefix, and then remove prefix
    reference_namespaces = [reference.removeprefix(RIG_REFERENCE_PREFIX) for reference in reference_namespaces
                            if reference.startswith(RIG_REFERENCE_PREFIX)]

    return reference_namespaces

def remove_rig_references_by_namespace(reference_namespaces: list[str]):
    references_to_remove = [reference for reference in cmds.ls(type='reference')
                            if cmds.referenceQuery(reference, namespace=True,
                                                   shortName=True).removeprefix(RIG_REFERENCE_PREFIX)
                            in reference_namespaces]

    for reference in references_to_remove:
        cmds.file(removeReference=True, referenceNode=reference)