from core.base_page import BasePage

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
        pass
        
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
        