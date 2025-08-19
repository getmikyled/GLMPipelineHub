import os
import glm.core.os.path as glm_path

REPOSITORY_DIR = glm_path.get_parent_directory(__file__, 4)
IMAGES_DIR = os.path.join(glm_path.get_parent_directory(__file__, 2), 'images')