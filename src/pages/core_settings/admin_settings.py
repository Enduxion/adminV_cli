from core.base_page import BasePage
from core.api import Api

class AdminSettings(BasePage):
    def __init__(self):
        super().__init__()
        self.menu = [
            {
                "key": "A",
                "name": "Add user"
            },
            {
                "key": "R",
                "name": "Remove user"
            },
            {
                "key": "C",
                "name": "Change permission"
            },
            {
                "key": "B",
                "name": "Back"
            },
        ]
        
    def add_user(self):
        while True:
            self.gui.clear
            print("Do you want to add new user? (y/n)")
            dec = self.gui.lis.lower()
            
            if dec == 'n':
                break
            elif dec != 'y':
                continue
            
            self.gui.print_table(Api().all_users(), ("Username", "Admin"))
            
            new_username = input(self.acc("New user's username: "))
            new_password = input(self.acc("New user's password: "))
            new_retry_password = input(self.acc("Retry new user's password: "))
            
            if new_password != new_retry_password:
                print(self.err("Passwords do not match"))
                self.gui.lis
                break
            
            print(self.acc("New user's permission: (y/n)"))
            dec2 = self.gui.lis.lower()
            new_is_admin = False
            
            if dec2 == "y":
                print("Permission: admin")
                new_is_admin = True
            else:
                print("Permission: non-admin")
            
            is_added = Api().add_user(new_username, new_password, new_is_admin)
            
            if not is_added:
                self.log(f"{self.state.user.username} couldn't add user {new_username}", "ERROR")
                print(self.err(f"Failed to add new user\nEnter {self.bold("h")} to see the potential reasons."))
                dec3 = self.gui.lis.lower()
                if dec3 == 'h':
                    self.gui.clear
                    print(f"Username can't be {self.bold("admin")}\nUsername can't be {self.bold("already in use")}\nUsername can only be {self.bold("alphabetic")}")
                    self.gui.lis
                break
            
            print(self.corr(f"Successfully added user: {self.bold(new_username)}"))
            self.gui.lis
            break
        
    def remove_user(self):
        while True:
            self.gui.clear
            print("Do you want to remove user? (y/n)")
            dec = self.gui.lis.lower()
            if dec == 'n':
                break
            elif dec != 'y':
                continue
            
            self.gui.print_table(Api().all_users(), ("Username", "Admin"))

            new_username = input(self.acc("Username of the user you want to remove: "))
            
            if new_username == self.state.user.username:
                print(self.err("Can't remove while logged in!\nRequest other admin user to remove the account!"))
                self.gui.lis
                break
            
            password = input(self.acc(f"(admin) Password of {self.state.user.username}: "))
            
            if not Api().is_logged_in(self.state.user.username, password):
                print(self.err("Incorrect Password!"))
                self.gui.lis
                break
            
            print("The user and all of their data will be removed", self.err(f"Do you really want to continue? (y/n)"), sep="\n")
            while True:
                dec2 = self.gui.lis.lower()
                
                if dec2 == 'n':
                    return
                elif dec2 == 'y':
                    break
            
            is_removed = Api().remove_user(new_username)
            
            if not is_removed:
                self.log(f"{self.state.user.username} couldn't remove user {new_username}", "ERROR")
                print(self.err(f"Some error occurred while removing user {new_username}"))
                self.gui.lis
                break
            
            print(self.corr(f"Removed {new_username} successfully!"))
            self.gui.lis
            break
    
    def change_permission(self):
        while True:
            self.gui.clear
            print("Do you want to change the permission of the users? (y/n)")
            dec = self.gui.lis.lower()
            
            if dec == 'n':
                break
            elif dec != 'y':
                continue
            
            all_users = Api().load_user_data()
            
            self.gui.print_table(Api().all_users(), ("Username", "Admin"))
            
            new_username = input(self.acc("Name of the user you want to change the permission of: "))
            
            if new_username == self.state.user.username:
                print(self.err("Can't change your own permission!"))
                self.gui.lis
                break
            
            if new_username not in all_users:
                print(self.err("Username not found!"))
                self.gui.lis
                break
            
            admin_vals = ("non-admin", "admin")
            admin_val = all_users[new_username]["is_admin"]
            
            print(f"Do you want to change the permission of {new_username} from {admin_vals[admin_val]} to {admin_vals[not admin_val]}? (y/n)")
            
            if self.gui.lis.lower == 'n':
                break
            
            is_changed = Api().change_permission(new_username)
            
            if not is_changed:
                self.log(f"{self.state.user.username} couldn't change the permission of {new_username}", "ERROR")
                print(self.err(f"Couldn't change the permission of {self.bold(new_username)}"))
                self.gui.lis
                break
            
            print(self.corr(f"Successfully changed the permission of {self.bold(new_username)} to {self.bold(admin_vals[not admin_val])}"))
            self.gui.lis
            break
            
    def run(self):
        self.gui.clear
        if not self.state.user.is_admin:
            print(self.err(f"Error: {self.bold(self.state.user.username)} does not have the permission to access this setting!"))
            self.gui.lis
            return
        
        while True:
            self.gui.clear
            self.gui.ls(self.menu)
            dec = self.gui.lis.lower()
            
            if dec == 'b':
                break
            elif dec == 'a':
                self.add_user()
            elif dec == 'r':
                self.remove_user()
            elif dec == 'c':
                self.change_permission()
        