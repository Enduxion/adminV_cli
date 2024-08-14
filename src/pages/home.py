from core.base_page import BasePage
from src.pages.settings import Settings
from src.pages.apps import Apps
class Home(BasePage):
    def __init__(self):
        super().__init__()
        self.menu = [
            {
                "key": "A",
                "name": "Applications"
            },
            {
                "key": "S",
                "name": "Settings"
            },
            {
                "key": "R",
                "name": "Restart"
            },
            {
                "key": "L",
                "name": "Log Out"
            },
            {
                "key": "Q",
                "name": "Shut down"
            }
        ]
        
    def run(self):
        while True:
            self.gui.clear
            self.gui.ls(self.menu)
            dec = self.gui.lis.lower()
            
            if dec == "q":
                return False
            elif dec == "l":
                self.loginfo(f"{self.state.user.username} logged out")
                return True
            elif dec == "r":
                self.loginfo(f"{self.state.user.username} restarted the computer")
                pass
            elif dec == "s":
                Settings().run()
            elif dec == "a":
                Apps().run()