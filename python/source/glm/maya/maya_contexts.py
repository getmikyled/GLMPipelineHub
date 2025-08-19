import contextlib
from contextlib import contextmanager
import maya.cmds as cmds

@contextlib.contextmanager
def restore_selection():
    """ Context manager to restore the user's selection in Maya.

    Usage:
        with restore_selection():
            # Modify the selection in some way
    """

    # Cache original selection
    original_selection = cmds.ls(selection=True)
    try:
        yield
    finally:
        # Restore selection if it still exists
        cmds.select(clear=True)
        for obj in original_selection:
            if cmds.objExists(obj):
                cmds.select(obj, add=True)
