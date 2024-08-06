from core.base_page import BasePage
from core.api import Api

class UserSettings(BasePage):
    def __init__(self):
        super().__init__()
        self.menu = [
            {
                "key": "C",
                "name": "Change Username"
            },
            {
                "key": "P",
                "name": "Change Password"
            },
            {
                "key": "L",
                "name": "List all users"
            },
            {
                "key": "B",
                "name": "Back"
            }
        ]
        
    def list_users(self):
        self.gui.clear
        headers = ("Username", "Admin")
        users = Api().all_users()
        self.gui.print_table(users, headers)
        print("Press any key to continue")
        self.gui.lis
        
    def change_username(self):
        while True:
            self.gui.clear
            print(f"Current username is: {self.bold(self.state.user.username)}\nDo you want to change it? (y/n)\n")
            dec = self.gui.lis.lower()              
            if dec == "n":
                break
            
            password = input(f"{self.acc("Verification\n")}Password for {self.bold(self.state.user.username)}: ")
            if not Api().is_logged_in(self.state.user.username, password):
                print(f"{self.err("Wrong password!")}")
                self.gui.lis
                break
            
            new_username = input(f"{self.acc("New Username: ")}")
            is_changed = Api().change_username(self.state.user.username, new_username)
            
            if not is_changed:
                print(f"Couldn't change the username.\nEnter {self.bold("h")} to see potential reason")
                deci = self.gui.lis.lower()
                if deci == "r":
                    self.gui.clear
                    print(f"Username can't be {self.bold("admin")}\nUsername can't be {self.bold("already in use")}\nUsername can only be {self.bold("alphabetic")}")
            break
            
    def run(self):
        while True:
            self.gui.clear
            self.gui.ls(self.menu)
            dec = self.gui.lis.lower()
            
            if dec == "b":
                break
            elif dec == "l":
                self.list_users()
            elif dec == "c":
                self.change_username()