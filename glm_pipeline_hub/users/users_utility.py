
def get_machine_id():
    """
    Gets the current user's machine ID.

    Returns:
         The unique machine identifier of type string.
    """

    import subprocess
    import platform

    system = platform.system()

    if system == 'Windows':
        cmd = "wmic csproduct get uuid"
        result = subprocess.check_output(cmd, shell=True).decode()
        lines = result.splitlines()
        uuid = lines[2]

    return uuid

def get_users():
    import json

    with open('users.json', 'r') as f:
        users = json.load(f)

        return users

def add_user(name):
    import json

    user_info = {
        'name': name,
        'blender_path': '',
        'maya_path': ''
    }

    users = get_users()

    machine_id = get_machine_id()
    users[machine_id] = user_info

    with open('users.json', 'w') as f:
        json.dump(users, f, indent=4)

print(get_machine_id())

add_user('Bruh')