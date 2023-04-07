import os
import time
import config
import json
import subprocess

def run_command(command):
    try:
        subprocess.run(command)
    except Exception as e:
        pass
    
def execute(command_id, item_path):
    file_lock = os.path.join(config.HOME_PATH, f"{command_id}.lock")
    file_data = os.path.join(config.HOME_PATH, f"{command_id}.data")

    # Create file data if not exists
    if not os.path.exists(file_data):
        open(file_data, 'a').close()

    # Append path to end of file data
    with open(file_data, 'a') as fdata:
        fdata.write(f"{item_path}\n")

    if not os.path.exists(file_lock):
        with open(file_lock, "wt") as flock:
            time.sleep(3)
        
        with open(file_data, 'rt') as fdata, open(config.get_settings_path(), 'rt') as fsett:
            proxied_command = json.loads(fsett.read())['proxied_commands'][command_id]            
            item_paths = []
            for line in fdata.read().split("\n"):
                if line.strip():
                    item_paths.append(f"\"{line.strip()}\"")

            file_list = proxied_command['item_separator'].join(item_paths)
            command_to_execute = proxied_command['command'].replace("%FILES", file_list)
            run_command(command_to_execute)

        os.unlink(file_data)
        os.unlink(file_lock)