from core.user import User

import os, json

class State:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(State, cls).__new__(cls)
            cls._user = User("", False)
            cls._user_path = ""
            cls._user_config = {}
            cls.load_def_config()
        return cls._instance
    
    @property
    def user(self):
        return self._user
    
    @classmethod
    def load_def_config(cls):
        with open("disk/sys/default_config.json", "r") as dc:
            cls._user_config = json.load(dc)
    
    def set_user(self, username, is_admin):
        self._user = User(username, is_admin)
        self._user_path = os.path.join("disk", "usr", self._user.username)
        self._load_user_config()

    def _load_user_config(self):
        with open(os.path.join(self._user_path, ".config"), "r") as config_file:
            self._user_config = json.load(config_file)

    @property
    def user_config(self):
        return self._user_config