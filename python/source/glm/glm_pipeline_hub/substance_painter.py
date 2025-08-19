# Property of Guardian's Lament
# Author: Mikyle Mosquera
# 2025Q3

import os
import shutil
import glm.core.users.users_utils as users_util

DRIVE_SUBSTANCE_EXPORT_PRESETS_DIR = r'G:\Shared drives\GLM\02_ASSETS\__IMPORTANT_FILES\SUBSTANCE\EXPORT_PRESETS'

def startup():
    refresh_export_presets()

def refresh_export_presets():
    """Update export presets in the local Substance Painter directory."""

    # Check if the user has been registered yet
    if users_util.get_users().get(users_util.get_machine_id()) is None:
        return

    destination_substance_export_presets_dir = os.path.join(
        users_util.get_users()[users_util.get_machine_id()].get(users_util.LOCAL_SUBSTANCE_PAINTER_USER_ATTR, ''),
        'assets\export-presets')

    # Verify if directories exist
    if not DRIVE_SUBSTANCE_EXPORT_PRESETS_DIR or not os.path.exists(DRIVE_SUBSTANCE_EXPORT_PRESETS_DIR):
        print(f'Substance painter export presets destination directory does not exist - '
                      + DRIVE_SUBSTANCE_EXPORT_PRESETS_DIR)
        return

    if not destination_substance_export_presets_dir or not os.path.exists(destination_substance_export_presets_dir):
        print(f'Substance painter export presets destination directory does not exist - '
                      + destination_substance_export_presets_dir)
        return

    # Iterate on all the files from the drive directory
    for drive_file in os.listdir(DRIVE_SUBSTANCE_EXPORT_PRESETS_DIR):
        if drive_file.endswith('.spexp'):
            # Get drive and destination file paths
            drive_file_path = os.path.join(DRIVE_SUBSTANCE_EXPORT_PRESETS_DIR, drive_file)
            dest_file_path = os.path.join(destination_substance_export_presets_dir, drive_file)

            # If the file exists, update if there are new changes
            if os.path.exists(dest_file_path):
                drive_mtime = os.path.getmtime(drive_file_path)
                dest_mtime = os.path.getmtime(dest_file_path)
                if drive_mtime > dest_mtime:
                    shutil.copy2(drive_file_path, dest_file_path)

            # Copy over file directly if the file does not exist
            else:
                shutil.copy2(drive_file_path, dest_file_path)

