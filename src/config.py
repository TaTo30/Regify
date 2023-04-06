import json

from pathlib import Path

HOME_PATH = Path.joinpath(Path.home(), ".regify")   
SETTINGS_FILE = "settings.json"
ICONS_FOLDER = "icons"

develop_mode = False
proxy_mode = False

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

def get_settings_path():
    path = Path.joinpath(HOME_PATH, SETTINGS_FILE)
    try: 
        if not Path.exists(path):
            with open(path, 'wt') as w_setting_file:
                w_setting_file.write(json.dumps({'proxied_commands': {}}, indent=2))
        return path
    except Exception as e:
        return False

_check_app_directory()
