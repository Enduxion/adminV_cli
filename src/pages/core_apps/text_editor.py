from core.base_page import BasePage
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
    
    def document_writer(self, pre="", pre_path=""):
        pre_path = os.path.join("disk", "usr", self.state.user.username, "exp")
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
        wait = False
        wait2 = False
        while True:
            #render
            self.gui.clear
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
                pass # Saving logic
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
            
            