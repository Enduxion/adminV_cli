from core.base_page import BasePage
from core.api import Api

class DiskSettings(BasePage):
    def __init__(self):
        super().__init__()
        self.menu = [
            {
                "key": "F",
                "name": "Format Disk"
            },
            {
                "key": "O",
                "name": "Backup Data"
            },
            {
                "key": "L",
                "name": "Load Data"
            },
            {
                "key": "R",
                "name": "Remove App"
            },
            {
                "key": "I",
                "name": "Install App"
            },
            {
                "key": "B",
                "name": "Back"
            }
        ]

        
    def run(self):
        while True:
            self.gui.clear
            self.gui.ls(self.menu)
            dec = self.gui.lis.lower()
            
            
            