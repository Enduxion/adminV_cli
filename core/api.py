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