from core.gui import Gui
from core.state import State
from functools import partial

class BasePage:
    def __init__(self):
        self.gui = Gui()
        self.state = State()
        self.err = partial(self.gui.colored, color=self.state.user_config["colors"]["_ec"])

    def run(self):
        raise NotImplementedError("Run has to be implemented")