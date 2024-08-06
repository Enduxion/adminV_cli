from core.base_page import BasePage
from src.pages.core_settings import user_settings as setting

class Settings(BasePage):
    def __init__(self):
        super().__init__()
        self.menu = [
            {
                "key": "U",
                "name": "User Settings"
            },
            {
                "key": "A",
                "name": "Admin Settings"
            },
            {
                "key": "T",
                "name": "Themes"
            },
            {
                "key": "D",
                "name": "Disk settings",
            },
            {
                "key": "L",
                "name": "Logs"
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
            
            if dec == "b":
                break
            elif dec == "l":
                # TODO: show logs
                pass
            elif dec == "d":
                # TODO: make disk settings
                pass
            elif dec == "t":
                # TODO: make theme
                pass
            elif dec == "a":
                # TODO: make admin
                pass
            elif dec == "u":
                setting.UserSettings().run()