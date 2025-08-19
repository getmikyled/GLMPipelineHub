import bpy
import sys
import time
import os

# --- Get arguments passed after `--`
argv = sys.argv
if "--" in argv:
    args = argv[argv.index("--") + 1:]
else:
    args = []

# --- Validate args
if len(args) < 2:
    print("Usage: blender --background --python your_script.py -- <blend_path> <import_path>")
    sys.exit(1)

character_name = args[0]
blend_path = args[1]
import_path = args[2]

# Create directory for blend if it doesn't exist
os.makedirs(os.path.dirname(blend_path), exist_ok=True)

print(f"Saving .blend to: {blend_path}")
print(f"Importing file: {import_path}")

# --- Reset scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# --- Create collection
anim_collection = bpy.data.collections.new(f'{character_name}_ANIM')
bpy.context.scene.collection.children.link(anim_collection)
anim_collection_layer = bpy.context.view_layer.layer_collection.children[0]
bpy.context.view_layer.active_layer_collection = anim_collection_layer

# --- Import the file (based on extension)
ext = os.path.splitext(import_path)[1].lower()

if ext == ".usd":
    bpy.ops.wm.usd_import(
        filepath=import_path,
        scale=1.0,
        set_frame_range=True,
        import_cameras=True,
        import_lights=True,
        import_materials=True,
        import_meshes=True,
        import_curves=True
    )
else:
    print(f"Unsupported import format: {ext}")
    sys.exit(1)

# --- Save to .blend
bpy.ops.wm.save_as_mainfile(filepath=blend_path)

print("Done. Waiting 10 seconds before exit...")
time.sleep(10)