import regedit
import config
import base64
import uuid
import io
import logging
import os

from PIL import Image, UnidentifiedImageError

logger = logging.getLogger(__name__)

class Command():
    def __init__(self, command = None, mui_verb = None, icon = None, keyname = None) -> None:
        self.keyname = keyname or str(uuid.uuid4()).split("-")[0]
        self.command = command
        self.mui_verb = mui_verb
        self.icon = self.icon_path(icon)

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
            "mui_verb": self.mui_verb,
            "icon": str(self.icon) if self.icon else self.icon
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
            regedit.add_command(self.keyname, self.command, self.mui_verb, self.icon)
        except Exception as e:
            return str(e)

    def __str__(self) -> str:
        return f"[{self.keyname}] {self.mui_verb} = {self.command} (icon = {self.icon})"


def commands():
    commands = []
    for cmd in regedit.get_commands():
        commands.append(Command(cmd['command'], cmd['MUIVerb'], cmd['Icon'], cmd['key']))
    return commands