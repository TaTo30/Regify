import regedit
import config
import base64
import uuid
import io
import logging
import os
import sys
import json

from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)

class Command():
    def __init__(self, command = None, command_id = None,
        mui_verb = None, icon = None, 
        keyname = None, multiple = False, item_separator = " ") -> None:

        self.keyname = keyname or str(uuid.uuid4()).split("-")[0]
        self.multiple = multiple
        self.item_separator = item_separator
        self.mui_verb = mui_verb
        self.command = command
        self.command_id = command_id or str(uuid.uuid4()).split("-")[0]
        self.icon = self.icon_path(icon)

    @property
    def proxy_command(self):
        logger.info(config.develop_mode)
        if config.develop_mode:
            return f"\"{sys.executable}\" \"{os.path.abspath(sys.argv[0])}\" \"-e\" \"{self.command_id}\" \"%1\""
        else:
            return f"\"{sys.executable}\" \"-e\" \"{self.command_id}\" \"%1\""

    def icon_path(self, icon):
        if not icon:
            return None
        try:
            if os.path.isabs(icon):
                return icon
            else: 
                icon_bytes = base64.b64decode(icon)
                icon_path = os.path.join(config.get_icons_path(), f"{self.keyname}.ico")
                image = Image.open(io.BytesIO(icon_bytes))
                image.save(icon_path, 'ICO')
                return icon_path
        except UnidentifiedImageError as ie:
            logger.warning(ie)
            return None
        except:
            return None

    def json(self):
        return {
            "keyname": self.keyname,
            "command": self.command,
            "command_id": self.command_id,
            "mui_verb": self.mui_verb,
            "icon": str(self.icon) if self.icon else self.icon,
            "multiple": self.multiple,
            "proxy_command": self.proxy_command if self.multiple else "",
            "item_separator": self.item_separator
        }
    
    def remove(self):
        try:
            if not self.keyname:
                raise Exception("'keyname' no provided")
            regedit.remove_command(self.keyname)
            logger.info(f"{self.keyname} command removed")
            
            icon_path = os.path.join(config.get_icons_path(), f"{self.keyname}.ico")
            if os.path.exists(icon_path):
                os.remove(icon_path)
                logger.info("Asociated icon removed")
        except Exception as e:
            logger.warning(e)

    def save(self):
        try:
            if self.multiple:
                with open(config.get_settings_path(), 'r+t') as sett:
                    settings = json.loads(sett.read())
                    settings["proxied_commands"][self.command_id] = {
                        "command": self.command,
                        "item_separator": self.item_separator
                    }
                    sett.seek(0)
                    sett.truncate()
                    sett.write(json.dumps(settings, indent=2))
                regedit.add_command(self.keyname, self.proxy_command, self.mui_verb, self.icon, self.command_id)
            else:
                regedit.add_command(self.keyname, self.command, self.mui_verb, self.icon)
        except Exception as e:
            logger.error(e)
            return str(e)

    def __str__(self) -> str:
        return f"[{self.keyname}] {self.mui_verb} = {self.command} (icon = {self.icon})"


def commands():
    commands = []
    for cmd in regedit.get_commands():
        command_id = None
        multiple = False
        user_command = cmd['command']
        item_separator = " "
        if cmd['Proxied']:
            command_id = cmd['Proxied']
            multiple = True
            with open(config.get_settings_path(), 'rt') as sett:
                settings = json.loads(sett.read())
                user_command = settings['proxied_commands'][command_id]['command']
                item_separator = settings['proxied_commands'][command_id]['item_separator']
        
        command = Command(command=user_command, 
            mui_verb=cmd['MUIVerb'], icon=cmd['Icon'], 
            keyname=cmd['key'], multiple=multiple, command_id=command_id,
            item_separator=item_separator)
        commands.append(command)
    return commands