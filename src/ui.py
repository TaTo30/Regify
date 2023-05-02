import base64
import command

import tkinter
import tkinter.filedialog
import customtkinter
from tkinter import messagebox
from PIL import Image

data = [
    {
        "command": "\"C:\\Users\\Aldo_\\Documents\\Dev\\Regify\\dist\\main.exe\" \"-e\" \"64b72433\" \"%1\"",
        "mui_verb": "Escribir Argumentos",
        "multiple": True,
        "icon": False,
    }
]

class CommandFrame(customtkinter.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.item_list = []
        self.master = master

    def add(self, item):
        CLEAR = customtkinter.CTkImage(Image.open("resources/clear.png"))
        def delete_item():
            try:
                cmd = command.Command(keyname=item["keyname"])
                cmd.remove()
                messagebox.showinfo("Aviso", "Comando eliminado")
                self.master.draw_command_list()
            except Exception as e:
                pass

        def icon_item():
            if item["icon"]:
                return customtkinter.CTkImage(Image.open(item["icon"]))
            return None

        item_frame = customtkinter.CTkFrame(self, fg_color="#545456", corner_radius=5)
        item_frame.grid_columnconfigure(0, weight=1)
        item_frame.grid_columnconfigure(1, weight=3)
        item_frame.grid_columnconfigure(2, weight=3)
        item_frame.grid_columnconfigure(3, weight=1)
        item_frame.grid_columnconfigure(4, weight=1)
        item_frame.grid(row=len(self.item_list), column=0, pady=10, sticky="nsew")

        icon_label = customtkinter.CTkLabel(item_frame, image=icon_item(), text="")
        mui_verb_label = customtkinter.CTkLabel(item_frame, text=item["mui_verb"],
                                                font=("Microsoft Sans Serif", 14))
        command_text = customtkinter.CTkTextbox(item_frame, height=65, width=340, text_color="white", 
                                                font=("Consolas", 12))
        command_text.insert("1.0", item["command"])
        command_text.configure(state="disabled")

        delete_button = customtkinter.CTkButton(item_frame, text="", width=15,
                                                image=CLEAR, fg_color="transparent",
                                                hover_color="#646464", command=delete_item)
        icon_label.grid(row=0, column=0, sticky="w", padx=5)
        mui_verb_label.grid(row=0, column=1, columnspan=2, sticky="w")
        command_text.grid(row=1, column=0, columnspan=5,
                          sticky="w", padx=5, pady=5)
        delete_button.grid(row=0, column=4, sticky="e", padx=5, pady=5)

        if item["multiple"]:
            multiple_label = customtkinter.CTkLabel(item_frame, text="MULTIPLE", fg_color="#f44336",
                                                    corner_radius=5, height=20, font=(None, 10))
            multiple_label.grid(row=0, column=3, sticky="e")

 
        self.item_list.append(item)
        
class ListUI(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        PLUS_MATH = customtkinter.CTkImage(Image.open("resources/plus-math.png"))
        super().__init__(master, **kwargs)

        self.create_button = customtkinter.CTkButton(self, text="AGREGAR COMANDO", image=PLUS_MATH,
                                                     command=lambda: master.switch_to_create(),
                                                     fg_color="transparent", hover_color="#444446")
        self.create_button.grid(row=0, column=0, pady=5, padx=10, sticky="nsew")

        self.draw_command_list()


    def draw_command_list(self):
        self.command_list = CommandFrame(self, width=350, height=550)
        self.command_list.grid(row=1, column=0)
        self.get_commands()

    def get_commands(self):
        for cmd in command.commands():
            self.command_list.add(cmd.json())

class CreateUI(customtkinter.CTkFrame):
    def __init__(self, master, **kwargs):
        ARROW_LEFT = customtkinter.CTkImage(Image.open("resources/arrow-left.png"))
        super().__init__(master, **kwargs)

        self.b64_icon = False

        # Botones de opciones/navegacion
        self.command_list_button = customtkinter.CTkButton(self, text="VER LISTA DE COMANDOS",
                                                           command=lambda: master.switch_to_list(), width=350,
                                                           fg_color="transparent", anchor="w", image=ARROW_LEFT,
                                                           hover_color="#444446")
        self.create_command = customtkinter.CTkButton(self, text="CREAR", command=self.compute_data,
                                                      fg_color="#26A69A", hover_color="#1f8a80")
        # Nombre del comando
        self.mui_verb_text_label = customtkinter.CTkLabel(self, text="Nombre del comando")
        self.mui_verb_text = customtkinter.CTkEntry(self)
        # Opciones
        self.multiple_checkbox = customtkinter.CTkCheckBox(self, text="Multiples items", border_width=1)
        # Comando
        self.command_text_label = customtkinter.CTkLabel(self, text="Comando")
        self.command_text = customtkinter.CTkTextbox(self, height=75, font=("Consolas", 12))
        # Icono
        self.icon_label = customtkinter.CTkLabel(self, text="Icono y opciones")
        self.select_icon_button = customtkinter.CTkButton(self, command=self.select_file, text="SELECCIONAR ICONO")
        self.icon = customtkinter.CTkLabel(self, text="", image=self.get_no_image_icon())
        # Instrucciones
        self.notes_space = customtkinter.CTkLabel(self, text="")
        self.notes_label = customtkinter.CTkLabel(self, text="CONSIDERACIONES:")
        self.note_1_label = customtkinter.CTkLabel(self,
                                                   wraplength=350, justify="left",
                                                   text="1. Si activa la opción 'Multiples items' use la variable %FILES para referenciar la lista de items seleccionados")
        self.note_11_label = customtkinter.CTkLabel(self,
                                                    font=("Consolas", 12),
                                                    text='"C:/App.exe" "--files" %FILES')
        # Layout
        self.command_list_button.grid(row=0, column=0, columnspan=3, pady=5, padx=10, sticky="nsew")

        self.mui_verb_text_label.grid(row=1, column=0, columnspan=3, sticky="w", padx=10)
        self.mui_verb_text.grid(row=2, column=0, columnspan=3, sticky="we", padx=10, pady=5)

        self.command_text_label.grid(row=3, column=0, columnspan=3, sticky="w", padx=10)
        self.command_text.grid(row=4, column=0, columnspan=3, sticky="we", padx=10)

        self.icon_label.grid(row=5, column=0, columnspan=3, sticky="w", padx=10)
        self.icon.grid(row=6, rowspan=2, column=0, sticky="we", padx=10, pady=5)
        self.select_icon_button.grid(row=6, column=1, columnspan=2, sticky="we", padx=10, pady=5)
        self.multiple_checkbox.grid(row=7, column=1, columnspan=2, sticky="w", padx=10, pady=5)

        self.notes_space.grid(row=8, padx=30)
        self.notes_label.grid(row=9, columnspan=3, sticky="w", padx=15)
        self.note_1_label.grid(row=10, columnspan=3, sticky="w", padx=5)
        self.note_11_label.grid(row=11, columnspan=3, sticky="w", padx=5)

        self.create_command.grid(row=12, column=0, columnspan=3, sticky="we", padx=10, pady=20)

    def compute_data(self):
        mui_verb = self.mui_verb_text.get()
        command_text = self.command_text.get(index1="1.0", index2="end-1c")
        multiple = bool(self.multiple_checkbox.get())
        icon = self.b64_icon

        if mui_verb and command_text:
            cmd = command.Command(command=command_text, 
                            mui_verb=mui_verb, 
                            multiple=multiple, 
                            icon=icon)
            cmd.save()
            self.clear_data()
            messagebox.showinfo("Comando creado", "El comando ha sido creado")
            

    def get_no_image_icon(self):
        return customtkinter.CTkImage(Image.open("resources/no-image.png"), size=(50, 50)) 
    
    def clear_data(self):
        self.mui_verb_text.delete(0, "end")
        self.command_text.delete("1.0", "end-1c")
        if self.b64_icon:
            self.b64_icon = False
            icon_no_image = self.get_no_image_icon()
            self.icon.configure(True, image=icon_no_image)


    def select_file(self):
        file = tkinter.filedialog.askopenfile("r", filetypes=[
            ("ICO files", ".ico"),
            ("PNG files", ".png"),
            ("JPEG files", [".jpg", ".jpeg", ".jpe", ".jfif"])])
        if file:
            with open(file.name, 'rb') as icon_file:
                self.b64_icon = base64.b64encode(icon_file.read()).decode()

            file_selected = Image.open(file.name)
            icon_selected = customtkinter.CTkImage(
                file_selected, size=(50, 50))
            self.icon.configure(True, image=icon_selected)


class UI(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.geometry("370x600")
        self.resizable(False, False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_frame = CreateUI(self)
        self.create_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame = ListUI(self)
        self.main_frame.grid(row=0, column=0, sticky="nsew")

    def switch_to_create(self):
        self.create_frame.tkraise()

    def switch_to_list(self):
        self.main_frame.draw_command_list()
        self.main_frame.tkraise()


customtkinter.set_appearance_mode("dark")
