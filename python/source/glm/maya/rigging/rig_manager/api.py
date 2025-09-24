import os
import json

RIG_PRESETS_JSON_PATH = os.path.join(os.path.dirname(__file__), 'rig_presets.json')

RIG_PATH_KEY = 'Rig Path'
MODEL_PATHS_KEY = 'Model Paths'
DEFORMING_GEO_KEY = 'Deforming Geo'

def get_rig_presets() -> dict:

    with open(RIG_PRESETS_JSON_PATH, 'r') as f:
        return json.load(f)

def set_rig_presets(rig_presets: dict):

    with open(RIG_PRESETS_JSON_PATH, 'w') as f:
        json.dump(rig_presets, f, indent=4)