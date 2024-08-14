from core.gui import Gui
from core.state import State
from core.log import Log
from functools import partial

class BasePage:
    def __init__(self):
        self.gui = Gui()
        self.log = Log().log
        self.state = State()
        self.err = partial(self.gui.colored, color="_ec")
        self.acc = partial(self.gui.colored, color="_ac")
        self.bold = partial(self.gui.styled, style="bold")
        self.corr = partial(self.gui.colored, color="_cc")
        self.logerr = partial(self.log, type_of_message="ERROR")
        self.loginfo = partial(self.log, type_of_message="INFO")

    def run(self):
        raise NotImplementedError("Run has to be implemented")