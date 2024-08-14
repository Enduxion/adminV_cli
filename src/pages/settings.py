from core.base_page import BasePage
from src.pages.core_settings import user_settings, admin_settings, theme_settings, disk_settings
from core.api import Api

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
                self.gui.clear
                Api().cat_log(self.state.user.username)
                self.gui.lis
                continue
            elif dec == "d":
                disk_settings.DiskSettings().run()
            elif dec == "t":
                theme_settings.ThemeSettings().run()
            elif dec == "a":
                admin_settings.AdminSettings().run()
            elif dec == "u":
                user_settings.UserSettings().run()