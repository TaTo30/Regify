import json

from pathlib import Path

HOME_PATH = Path.joinpath(Path.home(), ".regify")   
SETTINGS_FILE = "settings.json"
ICONS_FOLDER = "icons"

def _check_app_directory():
    if not Path.exists(HOME_PATH):
        Path.mkdir(HOME_PATH)
        print(f"{HOME_PATH} created")

def get_icons_path():
    path = Path.joinpath(HOME_PATH, ICONS_FOLDER)
    try: 
        if not Path.exists(path):
            Path.mkdir(path)
            return path
        return path
    except Exception as e:
        return False

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
            w_setting_file.write(json.dumps({'commands': {}}, indent=2))
        return False
    
def set_settings(settings):
    path = Path.joinpath(HOME_PATH, SETTINGS_FILE)
    with open(path, 'wt') as settings_file:
        settings_file.write(json.dumps(settings, indent=2))


_check_app_directory()
