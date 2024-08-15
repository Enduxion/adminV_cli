from cryptography.fernet import Fernet
from core.log import Log
import os
import json
import re
import time
import subprocess

PATT = r'^[A-Za-z]+$'

class Api:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Api, cls).__new__(cls)
            cls._sys_path = os.path.join("disk", "sys")
            cls.log = Log().log
            cls._default_dirs = (
                "apps",
                "backup",
                "exp",
            )
            cls._instance._key = cls.load_key()
            cls._instance._cypher_suite = Fernet(cls._instance._key)
        return cls._instance
    
    @classmethod
    def load_key(cls):
        cls.log("Loading key")
        try:
            with open(os.path.join(cls._sys_path, "vars.dat"), "rb") as key_file:
                key = key_file.read().strip()
                cls.log("Loaded key successfully")
                return key
        except Exception as e:
            cls.log("Error key couldn't load", "ERROR")
            raise RuntimeError("Failed to load encryption key.") from e

    def load_user_data(self):
        try:
            with open(os.path.join(self._sys_path, "usrdata.dat"), 'rb') as usrdata_file:
                encrypted_data = usrdata_file.read()
            
            decrypted_data = self._cypher_suite.decrypt(encrypted_data).decode()
            user_data = json.loads(decrypted_data)
            return user_data
        except Exception as e:
            self.log("Failed to load or decrypt user data", "ERROR")
            raise RuntimeError("Failed to load or decrypt user data.") from e

    def is_logged_in(self, username, password):
        user_data = self.load_user_data()
        if username in user_data:
            if password == user_data[username]["password"]:
                self.log(f"Successfully verified user {username}")
                return { "username": username, "is_admin": user_data[username]["is_admin"] }
        self.log(f"Unsuccessfull attempt at logging in as {username}")
        return None
    
    def all_users(self):
        user_data = self.load_user_data()
        new_user_data = []
        
        for keys in user_data:
            new_user_data.append((keys, user_data[keys]["is_admin"]))
            
        return new_user_data
        
    def change_username(self, username, new_username):
        all_users = self.load_user_data()
        
        if not re.search(PATT, new_username):
            return False
        if len(new_username) < 4 or len(new_username) > 10:
            return False
        
        if new_username != username and new_username in all_users:
            return False
        
        if username in all_users:
            data = all_users[username]
            del all_users[username]
            all_users[new_username] = data
            
        try:
            json_enc_data = self._cypher_suite.encrypt(json.dumps(all_users).encode())
            
            ## change the username in the dat file
            with open(os.path.join(self._sys_path, "usrdata.dat"), 'wb') as data_file:
                data_file.write(json_enc_data)
            
            ## change the exp folder name
            usr_path = os.path.join("disk", "usr")
            os.rename(os.path.join(usr_path, username), os.path.join(usr_path, new_username))
        except Exception:
            return False
        
        self.log(f"{username} changed username to {new_username}")
        return True
    
    def change_password(self, username, new_password):
        all_users = self.load_user_data()
        
        if username in all_users:
            all_users[username]["password"] = new_password
        else: return False
            
        try:
            json_enc_data = self._cypher_suite.encrypt(json.dumps(all_users).encode())
            
            ## change the password in the dat file
            with open(os.path.join(self._sys_path, "usrdata.dat"), 'wb') as data_file:
                data_file.write(json_enc_data)
        except Exception:
            return False
            
        self.log(f"{username} changed their password")
        return True
    
    def add_user(self, username, password, is_admin):
        all_users = self.load_user_data()
        
        if not re.search(PATT, username):
            print("Invalid username")
            return False
        if len(username) < 4 or len(username) > 10:
            print("Invalid length of the username")
            return False
        
        if username in all_users:
            print("Username already in use")
            return False
        
        print("Adding username in the list...")
        all_users[username] = { "password": password, "is_admin": is_admin }
        print("Success...")
        try:
            print("Encrypting data")
            json_enc_data = self._cypher_suite.encrypt(json.dumps(all_users).encode())
            print("Success...")
            
            
            print("Saving data")
            with open(os.path.join(self._sys_path, "usrdata.dat"), 'wb') as data_file:
                data_file.write(json_enc_data)
            print("Success...")
            file_path = os.path.join("disk", "usr", username)
            
            print("Creating user folder")
            os.makedirs(file_path)
            print("Success...")
            
            print("Creating folders")
            for folder_dir in self._default_dirs:
                print(f"Creating {folder_dir}")
                os.makedirs(os.path.join(file_path, folder_dir))
            print("Success...")
            
            print("Configuring user settings")
            os.system(f"cp {os.path.join("disk", "sys", "default_config.json")} {os.path.join(file_path, ".config")}")
            print("Success...")
        except Exception:
            print("Couldn't complete the setup!\nReverting the changes")
            self.remove_user(username)
            return False
        
        self.log(f"A new user with username={username} added with permission admin={is_admin}")
        return True
        
    def remove_user(self, username):
        all_users:dict[str, dict] = self.load_user_data()
        
        if username not in all_users:
            print(f"No user by the username {username}")
            return False
        
        is_current_user_admin = all_users[username]["is_admin"]
        
        admin_count = 0
        
        if is_current_user_admin:
            for key, val in all_users.items():
                if val["is_admin"]: admin_count += 1
                if admin_count > 1: break
                
        if admin_count < 2 and is_current_user_admin:
            print("Can't remove the only admin user!")
            return False
        
        print("Removing user")
        all_users.pop(username)
        print("Success...")
        
        try:
            print("Encrypting the data")
            json_enc_data = self._cypher_suite.encrypt(json.dumps(all_users).encode())
            print("Success...")
            
            print("Saving data")
            with open(os.path.join(self._sys_path, "usrdata.dat"), 'wb') as data_file:
                data_file.write(json_enc_data)
            print("Success...")
            
            file_path = os.path.join("disk", "usr", username)
            
            print("Removing the data")
            os.system(f"rm -r {file_path}")
            print("Success...")
        except Exception:
            return False
        
        self.log(f"Removed user {username}")
        return True
    
    def change_permission(self, username):
        all_users = self.load_user_data()
        
        if username not in all_users:
            return False
        
        admin_count = 0
        
        for key, val in all_users.items():
            if val["is_admin"]: admin_count += 1
            if admin_count > 1: break
            
        if admin_count < 2 and all_users[username]["is_admin"]:
            print("Can't change the permission of the only admin!")
            return False
        
        print("Changing the permission")
        all_users[username]["is_admin"] = not all_users[username]["is_admin"]
        print("Success...")
        
        try:
            print("Encrypting data")
            json_enc_data = self._cypher_suite.encrypt(json.dumps(all_users).encode())
            print("Success...")
            
            print("Saving data")
            with open(os.path.join(self._sys_path, "usrdata.dat"), "wb") as data_file:
                data_file.write(json_enc_data)
            print("Success...")
        except Exception:
            return False
        
        self.log(f"Changed permission of {username} to admin={all_users[username]["is_admin"]}")
        return True
    
    def reset_to_default(self, username):
        all_users = self.load_user_data()
        
        if username not in all_users:
            print(f"No user by the username {username}")
            
        try:
            def_config = None
            print("Reading default config")
            with open(os.path.join(self._sys_path, "default_config.json"), "r") as data_file:
                def_config = json.load(data_file)
                (def_config)
            print("Success...")
            
            print("Writing the new data")
            with open(os.path.join("disk", "usr", username, ".config"), "w") as data_file_2:
                data_file_2.write(json.dumps(def_config))
                
            print("Success...")    
                
        except Exception:
            return False
        
        return True
        
    def change_theme(self, username, theme_key, color_name):
        usr_config = None
        color_key = f"_{theme_key.lower()}c"
        try:
            with open(os.path.join("disk", "usr", username, ".config") , "r") as data_file:
                print("Loading the configuration")
                usr_config = json.load(data_file)
                print("Success...\nLoading the color to set")
                usr_config["colors"][color_key] = color_name.lower()
                print("Success...")
            
            with open(os.path.join("disk", "usr", username, ".config"), "w") as data_file:
                print("Saving data")
                data_file.write(json.dumps(usr_config))
                print("Success...")
            return True
        except Exception:
            return False
        
    def change_theme_config(self, username, theme_name):
        new_config = None
        configs = None
        
        try:
            with open(os.path.join(self._sys_path, "theme.json"), "r") as data_file:
                print(f"Loading {theme_name}!")
                configs = json.load(data_file)
                print("Success...\nConfiguring Settings")
                new_config = configs[theme_name.lower()]
                new_config = { "colors": new_config }
                print("Success...")
            with open(os.path.join("disk", "usr", username, ".config"), "w") as data_file:
                print("Saving data")
                data_file.write(json.dumps(new_config))
                print("Success...")
        except Exception:
            return False
        return True
    
    def backup(self, username, name):
        user_path = os.path.join("disk", "usr", username)
        
        try:
            print("Creating backup")
            title = name + '_' + f"{round(time.time() * 100)}"
            backup_dir = os.path.join(user_path, "backup", title)
            
            if os.path.isdir(backup_dir):
                print(f"Backup already exists with the name {title}")
                return False
            
            print("Creating directory")
            os.makedirs(backup_dir)
            print("Success....")
            
            print("Copying apps and explorer data")
            os.system(f"cp -r {os.path.join(user_path, 'apps')} {os.path.join(user_path, 'exp')} {backup_dir}")
            print("Success...\nCopying config")
            os.system(f"cp {os.path.join(user_path, ".config")} {backup_dir}")
            print("Success...")
            
            print(f"Made backup {title}")
            
        except Exception:
            return False

        self.log(f"{username} created a backup named {title}")
        return True
    
    def list_backup(self, username):
        user_path = os.path.join("disk", "usr", username, "backup")
        return os.listdir(user_path)            
    
    def format_disk(self, username):
        user_path = os.path.join("disk", "usr", username)
        
        try:
            print("Removing apps")
            os.system(f"rm -r {os.path.join(user_path, "apps")}")
            print("Success...")
            
            print("Removing all files")
            os.system(f"rm -r {os.path.join(user_path, "exp")}")
            print("Success...")
            
            print("Changing the theme to default")
            if self.reset_to_default(username):
                print("Success...")
            else:
                raise Exception
            
            print("Creating file exp and apps")
            os.makedirs(os.path.join(user_path, "apps"))
            os.makedirs(os.path.join(user_path, "exp"))
            print("Success...")
        except Exception:
            return False
        
        self.log(f"{username} formatted their disk")
        return True
    
    def load_backup(self, username, name):
        if name not in self.list_backup(username):
            return False
        
        path = os.path.join("disk", "usr", username)
        
        try:
            print("Removing existing files!")
            os.system(f"rm -r {os.path.join(path, "apps")} {os.path.join(path, "exp")}")
            print("Success...")
            print("Removing the config")
            os.system(f"rm {os.path.join(path, ".config")}")
            print("Success\nReverting the changes")
            os.system(f"cp -r {os.path.join(path, "backup", name, "apps")} {os.path.join(path, "backup", name, "exp")} {path}")
            print("Success...\nConfiguring")
            os.system(f"cp {os.path.join(path, "backup", name, ".config")} {path}")
            print("Success...")
        except Exception:
            return False
        
        self.log(f"{username} loaded backup with name {name}")
        return True
    
    def list_apps(self, username):
        path = os.path.join("disk", "usr", username, "apps")
        return os.listdir(path)
    
    def remove_app(self, username, name):
        if name not in self.list_apps(username):
            return False
        
        try:
            os.system(f"rm {os.path.join("disk", "usr", username, "apps", name)}")
        except Exception:
            return False
        
        return True
        
    def install_app(self, username, path):
        try:
            print("Checking the file path")
            if not os.path.isfile(path):
                print("File not found\nMake sure the path is an absolute path!")
                return False
            print("Success...")
            
            print("Checking the file type")
            if path[-4:].lower() != '.eux':
                print("Not a valid type of file!")
                return False
            
            print("Checking updates")
            app_name = path.split('/')[-1]

            for x in self.list_apps(username):
                if app_name.lower() == x.lower():
                    dec = input("App with same name was detected!\nDo you want to remove it and install the newer app?\nEnter 'y' to install or press any key to cancel\n").lower()
                    
                    if dec == 'y':
                        print("Removing the previous installation")
                        os.system(f"rm {os.path.join("disk", "usr", username, "apps", app_name)}")
                        print("Success...")
                        break
                    else:
                        print("Installation cancelled")
                        return False
            else:
                print("Fresh installation detected!")
                
            print("Installing the app!")
            os.system(f"cp {path} {os.path.join("disk", "usr", username, "apps")}")
            print("Success...")
            
            print(f"App successfully installed with app name {app_name}!")
        except Exception:
            return False
        return True
        
    def cat_log(self, username):
        self.log(f"{username} accessed log file")
        with open("./disk/log/__sys.log", "r") as log_file:
            print(log_file.read())
    
    def launch_app(self, username, app_name):
        load_app = f"{os.path.join("disk", "usr", username, "apps", app_name)}"
        print("Loading app...", load_app)
        subprocess.run(load_app)