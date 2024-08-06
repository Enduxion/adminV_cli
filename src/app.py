from core.state import State
from core.gui import Gui
from src.pages.all import Login, Home

class App:
    def __init__(self):
        self.state = State()

    def run(self):
        while True:
            user = Login().run()

            if user is None:
                break

            self.state.set_user(user["username"], user["is_admin"])
            Gui().reparam(self.state.user_config)
            
            cont = Home().run()
            
            if not cont:
                break
            
            