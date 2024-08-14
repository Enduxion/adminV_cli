from core.base_page import BasePage
from core.api import Api
from src.pages.core_apps.text_editor import TextEditor
from src.pages.core_apps.exp import Exp

class Apps(BasePage):
    def __init__(self):
        super().__init__()
        self.menu_items = ['/te (Text Editor)', '/exp (Explorer)'] + Api().list_apps(self.state.user.username)
        
    def run(self):
        while True:
            self.gui.clear
            print(f"Enter {self.bold('/q')} to exit")
            print(self.acc("-"*20))
            for x in self.menu_items:
                print(x)
            print(self.acc("-"*20))
            
            app_name = input("Enter the name of the app: ")
            
            if app_name.lower() == '/q':
                break
            elif app_name.lower() == '/te':
                TextEditor().run()
                break
            elif app_name.lower() == '/exp':
                Exp().run()
                break
                
            
            if app_name not in self.menu_items:
                print(self.err(f"No app by the name of {app_name}"))
                self.gui.lis
                continue
            
            app_loaded = Api().launch_app(self.state.user.username, app_name)
            
            if not app_loaded:
                print(self.err(f"There was an error loading {app_name}"))
                self.gui.lis
                continue
            
            