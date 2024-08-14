from core.state import State
from core.gui import Gui
from core.log import Log
from src.pages.all import Login, Home

class App:
    def __init__(self):
        self.state = State()
        Log().log("Computed started")

    def run(self):
        while True:
            print(Gui().reset)
            user = Login().run()

            if user is None:
                break

            self.state.set_user(user["username"], user["is_admin"])
            Gui().reparam(self.state.user_config)
            
            Log().log(f"Logged in as {user["username"]}")
            cont = Home().run()
            
            if not cont:
                break
        
        Gui().clear
        Gui().reset
        Log().log("Computed stopped")
            
            