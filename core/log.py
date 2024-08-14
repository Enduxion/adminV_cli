import time

class Log:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
            
        return cls._instance
    
    def log(self, message, type_of_message="INFO"):
        with open("./disk/log/__sys.log", "a") as log_file:
            log_file.write(f"[{type_of_message} {time.asctime()}]: {message}\n")