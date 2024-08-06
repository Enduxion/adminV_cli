from cryptography.fernet import Fernet
import os
import json

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