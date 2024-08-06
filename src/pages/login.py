from core.base_page import BasePage
from core.api import Api

class Login(BasePage):
    def __init__(self):
        super().__init__()

    def run(self):
        while True:
            self.gui.clear
            print(f"Enter {self.gui.styled(":q", "bold")} to exit!")
            username = input(f"Username:\n{self.gui.styled("=>", "dim")} ")
            
            if username.lower() == ":q":
                return None
            
            password = input(f"Password:\n{self.gui.styled("=>", "dim")} ")
            
            if password.lower() == ":q":
                return None

            user_data = Api().is_logged_in(username, password)

            if user_data:
                return user_data
            
            print(f"{self.gui.colored("Invalid credentials", "red")}\nPress 'q' to exit\nPress any key to continue")

            if self.gui.lis.upper() == "Q":
                return None
            
