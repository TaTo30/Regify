import base64
import regedit

from httpserver import app

if __name__ == "__main__":
    app.run()
    # regedit.remove_command("c3")
    # with open("favicon.png", "rb") as icon:
    #     iconb64 = base64.encodebytes(icon.read())
    #     regedit.add_command(
    #         keyname="c3", 
    #         command="C:\\Users\\Aldo_\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe",
    #         mui_verb="Testeando icono",
    #         icon="C:\\Users\\Aldo_\\Documents\\Dev\\Regify\\favicon.ico")
    
   
    
