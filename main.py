from src.app import App
from core.api import Api
from core.gui import Gui
import json

def check():
    boot_data = {}
    try:
        with open("disk/boot/.dat", "r") as boot:
            boot_data = json.load(boot)
    except:
        print(Gui().colored("FATAL ERROR: BOOT LOADING FAILED" ,"_ec"))
        exit(-1)
        
    if boot_data["unt"]:
        ## System is new
        boot_data["unt"] = False
    
        print("Saving instance")
        with open('disk/boot/.dat', 'w') as boot_:
            boot_.write(json.dumps(boot_data))
        print("Success...")
        print("Hello, welcome to adminV...")
        print("Creating boot vars and system protection vars...")
        print("Removing unwanted files")
        Api().remove_all()

        print(f"Default username and password are {Gui().styled("admin", "bold")} and {Gui().styled("password", "bold")}")
        Gui().lis
        Api().create_folders()
        
        print("Creating user: admin")
        added = Api().add_user("admin", "password", True)
        if not added:
            print("Error while adding user")
            exit(0)
        print("Press any key to contiue...")
        Gui().lis

def main():
    App().run()

if __name__ == "__main__":
    import time
    starttime = time.time()
    check()
    main()
    endtime = time.time()
    
    _time_ = endtime - starttime
    d = {}
    with open("disk/boot/.dat", "r") as bf:
        d = json.load(bf)
    d["ran"] = _time_
    d["syst"] += _time_
    with open("disk/boot/.dat", "w") as bf_:
        bf_.write(json.dumps(d))