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
    with winreg.CreateKey(hkey_context, APP_KEYBASE) as binding_context:
        winreg.SetValueEx(binding_context, "ExtendedSubCommandsKey", 0, winreg.REG_SZ, f"{APP_KEYBASE}\{APP_KEYBASE_COMMANDS}")
        winreg.SetValueEx(binding_context, "MUIVerb", 0, winreg.REG_SZ, APP_NAME)
        # winreg.SetValueEx(binding_directory, "Icon", 0, winreg.REG_SZ, )

def _unbind_context(hkey_context):
    winreg.DeleteKey(hkey_context, APP_KEYBASE)

def _bind_all_files():
    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, ALL_FILES_SHELL) as af_shell:
        _bind_context(af_shell)

def _bind_directory():
    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, DIRECTORY_SHELL) as d_shell:
        _bind_context(d_shell)

def _bind_background_directory():
    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, DIRECTORY_BACKGROUND_SHELL) as d_bg_shell:
        _bind_context(d_bg_shell)

def _unbind_all_files():
    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, ALL_FILES_SHELL) as af_shell:
        _unbind_context(af_shell)

def _unbind_directory():
    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, DIRECTORY_SHELL) as d_shell:
        _unbind_context(d_shell)

def _unbind_background_directory():
    with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, DIRECTORY_BACKGROUND_SHELL) as d_bg_shell:
        _unbind_context(d_bg_shell)

def bind_menu():
    _bind_all_files()
    _bind_background_directory()
    _bind_directory()

def unbind_menu():
    _unbind_all_files()
    _unbind_background_directory()
    _unbind_directory()

def add_command(keyname, command, mui_verb, icon):
    with winreg.CreateKey(_app_main_menu(), f"shell\{keyname}") as new_command:
        winreg.SetValue(new_command, "command", winreg.REG_SZ, command)
        winreg.SetValueEx(new_command, "MUIVerb", 0, winreg.REG_SZ, mui_verb)
        winreg.SetValueEx(new_command, "Icon", 0, winreg.REG_SZ, icon)

def remove_command(keyname):
    with winreg.OpenKey(_app_main_menu(), f"shell") as menu_shell:
        winreg.DeleteKey(menu_shell, f"{keyname}\\command")
        winreg.DeleteKey(menu_shell, keyname)
