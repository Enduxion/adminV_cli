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
        
    
    def run(self):
        while True:
            self.gui.clear
            print(self.acc("-"*20))
            for x in self.menu_items:
                print(x)
            print(self.acc("-"*20))
            
            dec = self.gui.lis.lower()
            
            if dec == 'q':
                break
            elif dec == 'q':
                break
            
            