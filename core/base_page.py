from core.gui import Gui
from core.state import State
from functools import partial

class BasePage:
    def __init__(self):
        self.gui = Gui()
        self.state = State()
        self.err = partial(self.gui.colored, color="_ec")
        self.acc = partial(self.gui.colored, color="_ac")
        self.bold = partial(self.gui.styled, style="bold")

    def run(self):
        raise NotImplementedError("Run has to be implemented")