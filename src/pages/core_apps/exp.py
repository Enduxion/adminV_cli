from core.base_page import BasePage
import os

class Exp(BasePage):
    def __init__(self):
        super().__init__()
        self.main_path = os.path.join("disk")
        self.current = self.main_path
        self.current_items : list[tuple] = []
        self.set_current_items()
        
    def set_current_items(self):
        self.current_items.clear()
        for item in os.listdir(self.current):
            self.current_items.append((
                item,
                "folder" if os.path.isdir(os.path.join(self.current, item)) else "file"
            ))        
    
    def run(self):
        while True:
            self.gui.clear
            self.gui.print_grid(self.current_items, headers=("Name","Type"))
            if self.gui.lis.lower() == "q": break
            
            