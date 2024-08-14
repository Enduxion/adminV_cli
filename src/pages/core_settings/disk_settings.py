from core.base_page import BasePage
from core.api import Api
import subprocess, os

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
        while True:
            self.gui.clear
            print("Do you want to make backup? (y/n)")
            dec = self.gui.lis.lower()
            
            if dec == 'n':
                break
            elif dec != 'y':
                continue
            
            backups = Api().list_backup(self.state.user.username)
            print("-"*20)
            for backup in backups:
                print(backup)
            
            print("-"*20)
            
            print(self.acc("Verification"))
            password = input("Password: ")
            
            if not Api().is_logged_in(self.state.user.username, password):
                print(self.err("Wrong password!"))
                self.gui.lis
                break
            
            name = input("Name of the backup (no space): ")
            if len(name.split(' ')) != 1:
                print(self.err("Space detected"))
                self.gui.lis
                break
            
            is_backedup = Api().backup(self.state.user.username, name)
            
            if not is_backedup:
                print(self.err("Some error occurred\nCouldn't backup"))
                self.gui.lis
                break
            
            print("Backed up data")
            self.gui.lis
            break
        
    def load_backup(self):
        while True:
            self.gui.clear
            
            print(self.acc("Verification"))
            password = input("Password: ")
            
            if not Api().is_logged_in(self.state.user.username, password):
                print(self.err("Wrong password!"))
                self.gui.lis
                break
            
            print("Load backup: ")
            for backup in Api().list_backup(self.state.user.username):
                print(backup)
            name_of_the_backup = input("Name of the backup (full): ")
            
            if not name_of_the_backup in Api().list_backup(self.state.user.username):
                print(self.err("Backup not found"))
                self.gui.lis
                break
            
            print(self.err("This will revert any changes to match the backup:\nDo you want to continue? (y/n)"))
            dec = self.gui.lis.lower()
            
            if dec == 'n':
                break
            elif dec != 'y':
                continue
            
            is_loaded = Api().load_backup(self.state.user.username, name_of_the_backup)
            
            if not is_loaded:
                print(self.err("Some error occurred while loading the backup"))
                self.gui.lis
                break
            
            print("Changing states")
            self.gui.reparam(self.state.user_config)
            print("Success...")
            print("Successfully loaded the backup")
            self.gui.lis
            break            
        
    def remove_app(self):
        while True:
            self.gui.clear
            print(f"Which app would you like to remove?\nEnter {self.bold(":q")} to go back")
            print("-"*20)
            for index, x in enumerate(Api().list_apps(self.state.user.username)):
                print(self.acc(f"{index + 1}. {x}"))
            print("-"*20)
            
            app_name = input("Enter the name of the application: ")
            if app_name.lower() == ":q":
                break
            
            if app_name not in Api().list_apps(self.state.user.username):
                print(self.err(f"No app by the name {app_name}"))
                self.gui.lis
                break
            
            is_removed = Api().remove_app(self.state.user.username, app_name)
            
            if not is_removed:
                print(self.err("Some error occurred while removing the app"))
                self.gui.lis
                break
            
            print(self.corr(f"Successfully removed {app_name}"))
            self.gui.lis
            break
        
    def install_app(self):
        while True:
            self.gui.clear
            print(self.acc("Verification"))
            password = input("Password: ")
            if not Api().is_logged_in(self.state.user.username, password):
                print(self.err("Wrong password!"))
                self.gui.lis
                break
            
            self.gui.clear
            print("-"*20)
            for index, x in enumerate(Api().list_apps(self.state.user.username)):
                print(self.acc(f"{index + 1}. {x}"))
            print("-"*20)
            
            path_to_app = input("Enter the path to the app: (separated by '/')")
            
            is_installed = Api().install_app(self.state.user.username, path_to_app)
            
            if not is_installed:
                print(self.err("Installation cancelled or some error occurred!"))
                self.gui.lis
                break
            
            print(self.corr("App installed!"))
            self.gui.lis
            break
                
        
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
            
            
            