from src.app import App
from core.api import Api
import json

def check():
    boot_data = {}
    with open("disk/boot/.dat", "r") as boot:
        boot_data = json.load(boot)
        
    if boot_data["unt"]:
        ## System is new
        print("Hello, welcome to adminV...")
        print("Creating boot vars and system protection vars...")
        print("Removing unwanted files")
        Api().remove_all()
        
        Api().generate_key()
        print("Default username and password are admin and password")
        Api().create_folders()
        
        print("Creating user: admin")
        added = Api().add_user("admin", "password", True)
        if not added:
            print("Error while adding user")
            exit(0)
            
        boot_data["unt"] = False
    
    print("Saving instance")
    with open('disk/boot/.dat', 'w') as boot_:
        boot_.write(json.dumps(boot_data))
    print("Success...")
    

def main():
    App().run()

if __name__ == "__main__":
    check()
    main()