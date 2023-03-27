import json

from pathlib import Path

HOME_PATH = Path.joinpath(Path.home(), ".regify")   
SETTINGS_FILE = "settings.json"

def _check_app_directory():
    if not Path.exists(HOME_PATH):
        Path.mkdir(HOME_PATH)
        print(f"{HOME_PATH} created")

def get_settings():
    path = Path.joinpath(HOME_PATH, SETTINGS_FILE)
    try: 
        with open(path, 'rb') as setting_file:
            settings = json.loads(setting_file.read())
            if not settings:
                return False
            return settings
    except Exception as e:
        # Create an empty settings.json
        with open(path, 'wt') as w_setting_file:
            w_setting_file.write(json.dumps({}, indent=2))
        return False

_check_app_directory()
