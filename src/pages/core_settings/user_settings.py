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
            elif dec != "y":
                continue
            
            password = input(f"{self.acc("Verification\n")}Password for {self.bold(self.state.user.username)}: ")
            if not Api().is_logged_in(self.state.user.username, password):
                print(f"{self.err("Wrong password!")}")
                self.gui.lis
                break
            
            new_username = input(f"{self.acc("New Username: ")}")
            is_changed = Api().change_username(self.state.user.username, new_username)
            
            if not is_changed:
                self.log(f"{self.state.user.username} couldn't change their username", "ERROR")
                print(self.err(f"Couldn't change the username.\nEnter {self.bold("h")} to see potential reason"))
                deci = self.gui.lis.lower()
                if deci == "h":
                    self.gui.clear
                    print(self.acc(f"Username can't be {self.bold("admin")}\nUsername can't be {self.bold("already in use")}\nUsername can only be {self.bold("alphabetic")}"))
                    self.gui.lis
                break
            
            print(f"{self.corr(f"Username successfully changed from {self.bold(self.state.user.username)} to {self.bold(new_username)}")}")
            self.state.set_user(new_username, self.state.user.is_admin)
            print("Press any key to continue")
            self.gui.lis
            break
    
    def change_password(self):
        while True:
            self.gui.clear
            print("Do you want to change the password? (y/n)")
            dec = self.gui.lis.lower()
            if dec == "n":
                break
            elif dec != "y":
                continue
            
            password = input(f"{self.acc("Verification\n")}Password for {self.bold(self.state.user.username)}: ")
            if not Api().is_logged_in(self.state.user.username, password):
                print(f"{self.err("Wrong password!")}")
                self.gui.lis
                break
            
            new_password = input(self.acc("New Password: "))
            retry_password = input(self.acc("Retype your password: "))
            
            if new_password != retry_password:
                print(f"{self.err("Passwords do not match!")}")
                self.gui.lis
                break
            
            is_changed = Api().change_password(self.state.user.username, new_password)
            
            if not is_changed:
                self.log(f"{self.state.user.username} couldn't change their password", "ERROR")
                print(f"{self.err("Couldn't change the password!")}")
                self.gui.lis
                break
            
            print(self.corr("Password successfully changed!"))
            print("Press any key to continue")
            self.gui.lis
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
            elif dec == "p":
                self.change_password()