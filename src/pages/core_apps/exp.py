from core.base_page import BasePage
import os, re

PATT = r'^[A-Za-z._-]+$'

class Exp(BasePage):
    def __init__(self):
        super().__init__()
        self.main_path = os.path.join("disk", "usr", self.state.user.username, "exp")
        if not os.path.isdir(self.main_path):            os.makedirs(self.main_path)
        self.current = self.main_path
        self.current_items : list[tuple] = []
        self.set_current_items()
        self.command_mode_activated = True
        
    def set_current_items(self):
        self.current_items.clear()
        for item in os.listdir(self.current):
            self.current_items.append((
                item,
                "folder" if os.path.isdir(os.path.join(self.current, item)) else "file"
            ))        
    
    def run(self):
        menu = [
            {
                "name": "Command mode",
                "key": "CTRL + C",
            },
            {
                "name": "Select mode",
                "key": "CTRL + S"
            },
            {
                "name": "Exit",
                "key": "CTRL + X"
            },
        ]
        menu2 = [
            {
                "name": "to exit command mode",
                "key": "exit"
            },
            {
                "name": "to show list of available commands",
                "key": "help"
            }
        ]
        while True:
            self.set_current_items()
            self.gui.clear
            
            if not self.command_mode_activated:
                self.gui.ls(menu)
            else:
                self.gui.ls(menu2)
            
            self.gui.print_grid(self.current_items, headers=("Name","Type"))
            print()
            dec = None
            if not self.command_mode_activated:
                dec = self.gui.lis
                
            if dec == '\x18':
                break
            elif dec == '\x13':
                pass
            elif dec == '\x03':
                self.command_mode_activated = not self.command_mode_activated
                continue
            
            if self.command_mode_activated:
                self.command_mode()
            
    def is_multi(self, command):
        if command.find('/') != -1 or command.find('\\') != -1:
            print(self.err("Multifolder system not allowed"))
            self.gui.lis
            return True
        
        if len(command) == 0:
            print(self.err("No args passed"))
            self.gui.lis
            return True
        
        if not re.match(PATT, command):
            print(self.err("Invalid name of the file or folder"))
            self.gui.lis
            return True
        return False
        
    def nav(self, command: str):
        command = command[3:].strip().strip("/")
        
        if self.is_multi(command):
            return
        
        if command == '..':
            paths = self.current.split(os.sep)
            if self.current == self.main_path:
                print(self.err("Permission denied!"))
                self.gui.lis
                return
            
            self.current = ""
            for index, x in enumerate(paths):
                if index < len(paths) - 1:
                    self.current = os.path.join(self.current, x)
            return
        
        if command == '.':
            return
        
        if command not in os.listdir(self.current):
            print(self.err(f"No folder by the name of {command}"))
            self.gui.lis
            return
        
        path = os.path.join(self.current, command)
        if not os.path.isdir(path):
            print(self.err(f"{command} is not a directory"))
            self.gui.lis
            return
                
        self.current = path
        
    def mdir(self, command: str):
        command = command[4:].strip()
        if self.is_multi(command):
            return
        
        if os.path.isdir(os.path.join(self.current, command)) or os.path.isfile(os.path.join(self.current, command)):
            print(self.err(f"File/Folder with the name {command} already exists"))
            self.gui.lis
            return
        
        try:
            os.makedirs(os.path.join(self.current, command))
        except Exception:
            print(self.err(f"Can't create folder: {command}"))
            self.gui.lis
        
    def rdir(self, command: str):
        command = command[4:].strip()
        if self.is_multi(command):
            return
        
        if not os.path.isdir(os.path.join(self.current, command)):
            print(self.err(f"{command} folder not found"))
            self.gui.lis
            return
        
        try:
            while True:
                self.gui.clear
                print(self.acc(f"Are you sure you want to remove {command}? (y/n)"))
                dec = self.gui.lis.lower()
                if dec == 'y':
                    break
                elif dec == 'n':
                    return
            os.system(f"rm -r {os.path.join(self.current, command)}")
        except Exception:
            print(self.err(f"Can't remove folder: {command}"))
            self.gui.lis
        
        return
    
    def mfile(self, command: str):
        command = command[5:].strip()
        if self.is_multi(command):
            return
        
        if os.path.isdir(os.path.join(self.current, command)) or os.path.isfile(os.path.join(self.current, command)):
            print(self.err(f"File/Folder with the name {command} already exists"))
            self.gui.lis
            return
        
        try:
            os.system(f"echo > {os.path.join(self.current, command)}")
        except Exception:
            print(self.err(f"Can't create file: {command}"))
            self.gui.lis
    
    def rfile(self, command: str):
        command = command[5:].strip()
        if self.is_multi(command):
            return
        
        if not os.path.isfile(os.path.join(self.current, command)):
            print(self.err(f"{command} file not found"))
            self.gui.lis
            return
        
        try:
            while True:
                self.gui.clear
                print(self.acc(f"Are you sure you want to remove {command}? (y/n)"))
                dec = self.gui.lis.lower()
                if dec == 'y':
                    break
                elif dec == 'n':
                    return
            os.system(f"rm {os.path.join(self.current, command)}")
        except Exception:
            print(self.err(f"Can't remove file: {command}"))
            self.gui.lis
    
    def show(self, command: str):
        command = command[4:].strip()
        if self.is_multi(command):
            return
        
        if not os.path.isfile(os.path.join(self.current, command)):
            print(self.err(f"{command} file not found"))
            self.gui.lis
            return
        
        try:
            with open(os.path.join(self.current, command), "r") as file_to_read:
                print(file_to_read.read())
        except Exception:
            print(self.err(f"There was a problem reading file: {command}"))
        
        self.gui.lis
    
    def command_mode(self): 
        command = input(self.bold(self.acc("(command > "))).strip()
        command_slices = command.split(" ")
        cs = command_slices[0].lower()
        if cs == "exit" or cs == "x" or cs == "quit":
            self.command_mode_activated = False
        elif cs == 'nav':
            self.nav(command)
        elif cs == 'mdir':
            self.mdir(command)
        elif cs == 'rdir':
            self.rdir(command)
        elif cs == 'mfile':
            self.mfile(command)
        elif cs == 'rfile':
            self.rfile(command)
        elif cs == 'show':
            self.show(command)
        elif cs == '~' or cs == '/':
            self.current = self.main_path
        elif cs == 'help':
            menu = [
                {
                    "name": "Navigate the exp",
                    "key": "nav <dir_name>"
                },
                {
                    "name": "make dir in the current folder",
                    "key": "mdir <dir_name>"
                },
                {
                    "name": "remove dir in the current folder",
                    "key": "rdir <dir_name>"
                },
                {
                    "name": "make file in the current folder",
                    "key": "mfile <file_name>"
                },
                {
                    "name": "remove file in the current folder",
                    "key": "rfile <dir_name>"
                },
                {
                    "name": "displays the content of the file",
                    "key": "show <file_name>"
                },
                {
                    "name": "exit command mode",
                    "key": "exit"
                },
                {
                    "name": "show list of commands",
                    "key": "help"
                }
            ]
            self.gui.ls(menu)
            self.gui.lis
        else:
            print(self.err(f"{self.bold(command)} not a command"))
            self.gui.lis
            
        
        