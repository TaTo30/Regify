import winreg

APP_KEYBASE = "Regify"
APP_KEYBASE_COMMANDS = "Commands"
DIRECTORY_SHELL = "Directory\\shell"
DIRECTORY_BACKGROUND_SHELL = "Directory\\background\\shell"
ALL_FILES_SHELL = "*\\shell"
APP_NAME = APP_KEYBASE

def _app_keybase():
    return winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, APP_KEYBASE)

def _app_main_menu():
    return winreg.CreateKey(_app_keybase(), APP_KEYBASE_COMMANDS)

def _bind_context(hkey_context):
    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, hkey_context) as shell:
        with winreg.CreateKey(shell, APP_KEYBASE) as binding_context:
            winreg.SetValueEx(binding_context, "ExtendedSubCommandsKey", 0, winreg.REG_SZ, f"{APP_KEYBASE}\{APP_KEYBASE_COMMANDS}")
            winreg.SetValueEx(binding_context, "MUIVerb", 0, winreg.REG_SZ, APP_NAME)
            # winreg.SetValueEx(binding_directory, "Icon", 0, winreg.REG_SZ, )

def _unbind_context(hkey_context):
    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, hkey_context) as shell:
        winreg.DeleteKey(shell, APP_KEYBASE)

def _bind_all_files():
    _bind_context(ALL_FILES_SHELL)

def _bind_directory():
    _bind_context(DIRECTORY_SHELL)

def _bind_background_directory():
    _bind_context(DIRECTORY_BACKGROUND_SHELL)

def _unbind_all_files():
    _unbind_context(ALL_FILES_SHELL)

def _unbind_directory():
    _unbind_context(DIRECTORY_SHELL)

def _unbind_background_directory():
    _unbind_context(DIRECTORY_BACKGROUND_SHELL)

def bind_menu():
    _bind_all_files()
    _bind_background_directory()
    _bind_directory()

def unbind_menu():
    _unbind_all_files()
    _unbind_background_directory()
    _unbind_directory()

def get_commands():
    with winreg.OpenKey(_app_main_menu(), "shell") as menu_shell:
        try: 
            index = 0
            while True:
                cmd_keystr = winreg.EnumKey(menu_shell, index)
                with winreg.OpenKey(menu_shell, cmd_keystr) as cmd:                    
                    yield {
                        "key": cmd_keystr,
                        "command": winreg.QueryValue(cmd, "command"),
                        "MUIVerb": winreg.QueryValueEx(cmd, "MUIVerb")[0],
                        "Proxied": winreg.QueryValueEx(cmd, "Proxied")[0],
                        "Icon":  winreg.QueryValueEx(cmd, "Icon")[0]
                    }
                index += 1
        except: 
            return

def add_command(keyname, command, mui_verb, icon, proxy = ""):
    with winreg.CreateKey(_app_main_menu(), f"shell\{keyname}") as new_command:
        winreg.SetValue(new_command, "command", winreg.REG_SZ, command)
        winreg.SetValueEx(new_command, "MUIVerb", 0, winreg.REG_SZ, mui_verb)
        winreg.SetValueEx(new_command, "Proxied", 0, winreg.REG_SZ, proxy)
        winreg.SetValueEx(new_command, "Icon", 0, winreg.REG_SZ, icon if icon else "")

def remove_command(keyname):
    with winreg.OpenKey(_app_main_menu(), f"shell") as menu_shell:
        winreg.DeleteKey(menu_shell, f"{keyname}\\command")
        winreg.DeleteKey(menu_shell, keyname)
