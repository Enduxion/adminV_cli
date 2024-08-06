from core.user import User

class State:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(State, cls).__new__(cls)
            cls._user = User("", "", False)
        return cls._instance
    
    @property
    def user(self):
        return self._user
    
    def set_user(self, username, password, is_admin):
        self._user = User(username, password, is_admin)