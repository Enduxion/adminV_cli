from cryptography.fernet import Fernet
import os
import json
import re

PATT = r'^[A-Za-z]+$'

class Api:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Api, cls).__new__(cls)
            cls._sys_path = os.path.join("disk", "sys")
            cls._instance._key = cls.load_key()
            cls._instance._cypher_suite = Fernet(cls._instance._key)
        return cls._instance
    
    @classmethod
    def load_key(cls):
        try:
            with open(os.path.join(cls._sys_path, "vars.dat"), "rb") as key_file:
                key = key_file.read().strip()
                return key
        except Exception as e:
            raise RuntimeError("Failed to load encryption key.") from e

    def load_user_data(self):
        try:
            with open(os.path.join(self._sys_path, "usrdata.dat"), 'rb') as usrdata_file:
                encrypted_data = usrdata_file.read()

            decrypted_data = self._cypher_suite.decrypt(encrypted_data).decode()
            user_data = json.loads(decrypted_data)
            return user_data
        except Exception as e:
            raise RuntimeError("Failed to load or decrypt user data.") from e

    def is_logged_in(self, username, password):
        user_data = self.load_user_data()
        if username in user_data:
            if password == user_data[username]["password"]:
                return { "username": username, "is_admin": user_data[username]["is_admin"] }
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
            
            print("making file dir")
            os.makedirs(file_path)
            print("Success...")
            
            print("Condifguring user settings")
            os.system(f"cp {os.path.join("disk", "sys", "default_config.json")} {os.path.join(file_path, ".config")}")
            print("Success...")
        except Exception:
            return False
        
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