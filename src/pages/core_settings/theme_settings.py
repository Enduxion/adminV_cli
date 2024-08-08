from core.base_page import BasePage
from core.api import Api

class ThemeSettings(BasePage):
    def __init__(self):
        super().__init__()
        self.menu = [
            {
                "key": "S",
                "name": "Built-in Schemes"
            },
            {
                "key": "C",
                "name": "Build it yourself"
            },
            {
                "key": "R",
                "name": "Reset to default"
            },
            {
                "key": "B",
                "name": "Back"
            }
        ]
        
    def reset_to_default(self):
        while True:
            self.gui.clear
            print(f"This will reset the theme of {self.state.user.username} to default\nDo you want to continue? (y/n)")
            
            dec = self.gui.lis.lower()
            
            if dec == 'n':
                break
            elif dec != 'y':
                continue
            
            print("Reseting...")
            Api().reset_to_default(self.state.user.username)
            self.gui.reset
            print(self.corr("Successfully reseted the theme!"))
            break
    
    def custom_built(self):
        menu = [
            {
                "key": "F",
                "name": "Foreground Color"
            },
            {
                "key": "A",
                "name": "Accent Color"
            },
            {
                "key": "E",
                "name": "Error Color"
            },
            {
                "key": "C",
                "name": "Correct Color"
            },
            {
                "key": "B",
                "name": "Back"
            }
        ]
        while True:
            self.gui.clear
            self.gui.ls(menu)
            dec = self.gui.lis.lower()
            
            if dec == 'b':
                break
            elif dec.upper() in list([val["key"] for val in menu]):
                name = next(val["name"] for val in menu if val["key"] == dec.upper())
                self.change_data(name, dec)
    
    def change_data(self, name, key):
        menu = ["Red", "Blue", "Green", "Yellow", "Magenta", "Cyan", "White"]
        
        while True:
            self.gui.clear
            print(f"Change the {name.lower()}")
            for index, item in enumerate(menu):
                print(f"{index + 1}. {item}")
            
            try:
                dec = int(self.gui.lis.lower())
            except Exception:
                continue
            
            if dec > 0 and dec <= len(menu):
                is_changed = Api().change_theme(self.state.user.username, key, menu[dec - 1])
                if not is_changed:
                    print(self.err("Some error occurred!"))
                    self.gui.lis
                    break
                
                self.gui.reparam(self.state.user_config)
                print(self.corr("Successfully changed the theme!"))
                self.gui.lis
                break
                
    def built_in_scheme(self):
        pass
    
    def run(self):
        while True:
            self.gui.clear
            self.gui.ls(self.menu)
            dec = self.gui.lis.lower()
            
            if dec == 'b':
                break
            elif dec == 'r':
                self.reset_to_default()
            elif dec == 'c':
                self.custom_built()
            elif dec == 's':
                self.built_in_scheme()
            