from core.base_page import BasePage
from src.pages.core_apps.exp import Exp
import os
class TextEditor(BasePage):
    def __init__(self):
        super().__init__()
        self.menu_items = [
            {
                "name": "New File",
                "key": "N"
            },
            {
                "name": "Open File",
                "key": "O"
            },
            {
                "name": "Quit",
                "key": "Q"
            }
        ]
    
    
    def save_text(self, text, path, filename):
        self.gui.clear
        if path != "" and filename != "":
            try:
                with open(path, "w") as file_data:
                    file_data.write(text)
                    
                print(self.corr(f"{filename} saved successfully"))
                self.gui.lis
                return True
            except Exception:
                print(self.err(f"There was an error saving file: {filename}"))
                self.gui.lis
        elif path == "" and filename == "":
            while True:
                self.gui.clear
                print("Select a file to save it there!\nIn Exp, if you want to have a new file, use sel <new_filename>")
                self.gui.lis
                path = Exp().run(True, True, True)
                
                try:
                    with open(path, "w") as file_data:
                        file_data.write(text)
                    print(self.corr(f"File saved in {path} successfully"))
                    self.gui.lis
                    return True
                except Exception:
                    print(self.err(f"There was an error saving file to path: {path}"))
                    self.gui.lis
                    continue
                
        return False
                
    
    def document_writer(self, pre="", pre_path=""):
        file_name = pre_path.split(os.sep)[len(pre_path.split(os.sep)) - 1]
        menu = [
            {
                "name": "Exit saving file",
                "key": "Ctrl + S",
            },
            {
                "name": "Exit without saving file",
                "key": "Ctrl + X"
            },
            {
                "name": "Delete all text",
                "key": "Ctrl + R",
            },
        ]
        self.gui.clear
        current_text = pre
        while True:
            #render
            self.gui.clear
            print(f"{self.acc(self.bold("TEXT EDITOR"))} {self.bold(f"- {file_name}" if pre_path != "" else "")}")
            self.gui.ls(menu)
            print(current_text, end="", flush=True)
            #update
            new_text = self.gui.lis
            if new_text == '\x18': # CTRL + X
                while True:
                    self.gui.clear
                    print("Do you want to quit without saving the file? (y/n)")
                    dec2 = self.gui.lis.lower()
                    if dec2 == 'n':
                        break
                    elif dec2 == 'y':
                        return
                    
            elif new_text == '\x13': # CTRL + S
                saved = self.save_text(current_text, pre_path, file_name)
                if not saved:
                    continue
                break
            elif new_text == '\x12': # CTRL + R
                current_text = ""
            elif new_text == '\r':
                current_text += '\n'
            elif new_text == '\x7f':
                current_text = current_text[:-1]
            else:
                current_text += new_text

    
    def run(self):
        while True:
            self.gui.clear
            self.gui.ls(self.menu_items)
            
            dec = self.gui.lis.lower()
            
            if dec == 'q':
                break
            elif dec == 'n':
                self.document_writer()
            elif dec == 'o':
                path_to_the_file = Exp().run(True, True, False)
                if path_to_the_file is None:
                    print(self.err(f"No file selected!"))
                    self.gui.lis
                    continue
                pre_data = ""
                with open(path_to_the_file, "r") as file_data:
                    pre_data = file_data.read()
                self.document_writer(pre_data, path_to_the_file)
            