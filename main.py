import os
import json
import sys
import getpass

from os.path import isfile
from hashlib import sha256
from termcolor import colored
from halo import Halo

from modules.encryption import DataManip
from modules.exceptions import UserExits, PasswordFileDoesNotExist
from modules.menu import Manager

from modules.frontend_connection import *

def exit_program():
    print(colored("Exiting...", "red"))
    sys.exit()

async def start(obj: DataManip):
    if os.path.isfile("db/masterpassword.json"):
        with open("db/masterpassword.json", 'r') as jsondata:
            jfile = json.load(jsondata)

        set_is_new(False)
        stored_master_pass = jfile["Master"] # load the saved hashed password
        master_password = simulate_input("Enter your Master password: ")

        # compare the two hashes of inputted password and stored
        spinner = Halo(text=colored("Unlocking", "green"), color="green", spinner=obj.dots_)
        if sha256(master_password.encode("utf-8")).hexdigest() == stored_master_pass:
            menu = Manager(obj, "db/passwords.json", "db/masterpassword.json", master_password)
            set_manager(menu)
            
            try:
                await alert_frontend("Success!")
                await menu.begin()
            except UserExits:
                exit_program()
            except PasswordFileDoesNotExist:
                print(colored(f"{obj.x_mark_} DB not found. Try adding a password {obj.x_mark_}", "red"))
        else:
            print(colored(f"{obj.x_mark_} Master password is incorrect {obj.x_mark_}", "red"))
            return start(obj)

    else: # First time running program: create a master password
        try:
            os.mkdir("db/")
        except FileExistsError:
            pass
        
        set_is_new(True)
        print(colored("To start, we'll have you create a master password. Be careful not to lose it as it is unrecoverable.", "green"))
        master_password = simulate_input("Enter your master password!: ")
        second_input = simulate_input("Verify your master pasword: ")

        if master_password == second_input:
            await alert_frontend("Success!")
            hash_master = sha256(master_password.encode("utf-8")).hexdigest()
            jfile = {"Master": {}}
            jfile["Master"] = hash_master

            with open("db/masterpassword.json", 'w') as jsondata:
                json.dump(jfile, jsondata, sort_keys=True, indent=4)
            
            
            return True
        else:
            print(colored(f"{obj.x_mark_} Passwords do not match. Please try again {obj.x_mark_}", "red"))
            return start(obj)




# threading.Thread(target=websocket_server, daemon=True).start()

async def main_loop():
    start_websocket_server_in_thread()
    obj = DataManip()
    should_start_again = await start(obj)

    if(should_start_again):
        obj = DataManip()
        await start(obj)

asyncio.run(main_loop())