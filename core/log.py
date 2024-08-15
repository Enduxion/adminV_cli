import time

TODAYS_DATE = f"{time.localtime().tm_year}_{time.localtime().tm_mon}_{time.localtime().tm_mday}"

class Log:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Log, cls).__new__(cls)
            
        return cls._instance
    
    def log(self, message, type_of_message="INFO"):
        with open(f"./disk/log/__sys-{TODAYS_DATE}.log", "a") as log_file:
            log_file.write(f"[{type_of_message} {time.asctime()}]: {message}\n")