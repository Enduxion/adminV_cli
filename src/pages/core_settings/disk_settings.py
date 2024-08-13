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
        
    def format_disk(self):
        while True:
            self.gui.clear
            print(self.err("This will remove all the contents of your disk\nDo you want to continue? (y/n)"))
            dec = self.gui.lis.lower()
            if dec == 'n':
                break
            elif dec != 'y':
                continue
            
            print(self.acc("Verification"))
            password = input("Password: ")
            if not Api().is_logged_in(self.state.user.username, password):
                print(self.err("Passwords do not match"))
                self.gui.lis
                break
            
            is_removed = Api().format_disk(self.state.user.username)
            if not is_removed:
                print(self.err("Some error occurred"))
                self.gui.lis
                break
            
            print(self.corr("Formatted disk successfully"))
            self.gui.lis
            break
    def backup(self):
        pass
        
    def load_backup(self):
        pass
        
    def remove_app(self):
        pass
        
    def install_app(self):
        pass
        
    def run(self):
        while True:
            self.gui.clear
            self.gui.ls(self.menu)
            dec = self.gui.lis.lower()
            if dec == 'b':
                break
            elif dec == 'f':
                self.format_disk()
            elif dec == 'o':
                self.backup()
            elif dec == 'l':
                self.load_backup()
            elif dec == 'r':
                self.remove_app()
            elif dec == 'i':
                self.install_app()
            
            
            