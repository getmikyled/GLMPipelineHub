import os
import subprocess
import glm.core.users.users_utils as users_utils

def create_animation_cache_blend_file(character_name: str, blend_path: str, import_path: str):
    blender_path = users_utils.get_users()[users_utils.get_machine_id()][users_utils.BLENDER_USER_ATTR]
    blender_exe = os.path.join(blender_path, 'blender.exe')

    # Path to your Blender Python script
    blend_script = r'G:\Shared drives\GLM\06_PIPELINE\python\source\glm\blender\background\create_animation_cache_blend_file.py'

    # Run Blender in background mode
    result = subprocess.run([
        blender_exe,
        '--background',
        '--python', blend_script,
        '--', character_name, blend_path, import_path
    ], capture_output=True, text=True)

    print(result.stdout)