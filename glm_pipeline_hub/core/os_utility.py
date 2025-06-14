import sys
import os

def get_resource_path(relative_path):
    """Returns the absolute path to a resource, works for pyinstaller."""

    try:
        # pyinstaller creates temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath('')

    return os.path.join(base_path, relative_path)