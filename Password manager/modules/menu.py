import sys
import getpass
import pyperclip
import json
from termcolor import colored
from halo import Halo

from modules.encryption import DataManip
from modules.exceptions import *
from modules.frontend_connection import *

class Manager:
    """
    Arguments: 
        obj {DataManip}
        filename {str}
        master_pass {str}
    """
    def __init__(self, obj: DataManip, filename: str, master_file: str, master_pass: str):
        self.obj_ = obj
        self.filename_ = filename
        self.master_file_ = master_file
        self.master_pass_ = master_pass

    async def begin(self):
        try:
            # NOTE: fully tested already
            choice = self.menu_prompt()
        except UserExits:
            raise UserExits

        if choice == '4': # User Exits
            raise UserExits

        if choice == '1': # add or update a password
            # NOTE: fully tested already
            try:
                await self.update_db()
                return await self.begin()
            except UserExits:
                raise UserExits
        
        elif choice == '2': # look up a stored password
            # NOTE: fully tested already

            print("Loading password...")
            string = await self.load_password()
            website = string.split(':')[0]
            password = string.split(':')[1]
            
            await alert_frontend(json.dumps({
                "password": password
            }))
            
            return await self.begin()


        elif choice == '3': # Delete a single password
            # NOTE: fully tested already
            try:
                return await self.delete_password()
            except UserExits:
                raise UserExits

        elif choice == '5': # Delete DB of Passwords
            # NOTE: fully tested already
            try:
                await self.delete_db(self.master_pass_)
            except MasterPasswordIncorrect:
                print(colored(f"{self.obj_.x_mark_} Master password is incorrect {self.obj_.x_mark_}", "red"))
                return await self.delete_db(self.master_pass_)
            except UserExits:
                raise UserExits
        
        elif choice == '6': # delete ALL data
            # NOTE: fully tested already
            print("DELETING")
            await self.delete_all_data(self.master_pass_)
            await self.begin()

                
                


    def menu_prompt(self):
        """Asks user for a choice from Menu
        
        Raises:
            UserExits: User exits on choice prompt
        
        Returns:
            str -- Users choice
        """

        print(colored("\n\t*Enter 'exit' at any point to exit.*\n", "magenta"))
        print(colored("1) Add/Update a password", "blue"))
        print(colored("2) Look up a stored password", "blue"))
        print(colored("3) Delete a password", "blue"))
        print(colored("4) Exit program", "blue"))
        print(colored("5) Erase all passwords", "red"))
        print(colored("6) Delete all data including Master Password", "red"))

        choice = simulate_input("Enter your choice: ")

        if choice == "":
            return self.menu_prompt() # recursive call
        elif choice == "exit":
            raise UserExits
        else:
            return choice.strip()

    def __return_generated_password(self, website):
        """Returns a generated password
        
        Arguments:
            website {str} -- website for password
        
        Raises:
            UserExits: User exits on loop prompt
        
        Returns:
            str -- A randomly generated password
        """

        try:
            generated_pass = self.obj_.generate_password()
            return generated_pass
        
        except:
            return ""
            

        
        
    async def update_db(self): # option 1 on main.py
        """Add or update a password in the DB
        
        Raises:
            UserExits: User enters exit at website prompt or generate prompt
        """

        website = simulate_input("Enter a website: ")
        
        if website.lower() == "":
            await self.update_db()
        elif website.lower().strip() == "exit":
            raise UserExits
        else:
            password = self.__return_generated_password(website)
            if len(password)==0:
                await alert_frontend("Fail")
            else:
                self.obj_.encrypt_data("db/passwords.json", password, self.master_pass_, website)
                await alert_frontend("Success!")
    
    async def load_password(self):
        """Loads a string of websites stored and asks user to enter a 
        website, then decrypts password for entered website
        
        Raises:
            PasswordFileDoesNotExist: DB is not initialized
            UserExits: User enters exit on website prompt
        
        Returns:
            str -- string formatted in website:password
        """
        website = simulate_input("Enter website for the password you want to retrieve: ")

        try:
            plaintext = self.obj_.decrypt_data(self.master_pass_, website, self.filename_)
            final_str = f"{website}:{plaintext}"

            return final_str
        except:
            await alert_frontend("Password doesnt exist")
            return f"{website}:PASSWORD NOT FOUND"
            
            # see https://pypi.org/project/clipboard/ for copying to clipboard
        

    async def delete_db(self, stored_master):
        """Menu Prompt to Delete DB/Passwords
        
        Arguments:
            stored_master {str} -- Used to authenticate, compared with inputted master password
        
        Raises:
            PasswordFileDoesNotExist: Password file not initialized
        """


        
        entered_master = simulate_input("Enter your master password to delete all stored passwords: ")

        try:
            self.obj_.delete_db(self.filename_, stored_master, entered_master)
            print(colored(f"{self.obj_.checkmark_} Password Data Deleted successfully. {self.obj_.checkmark_}", "green"))
            return await self.begin()
        
        except MasterPasswordIncorrect:
            raise MasterPasswordIncorrect
        
        except PasswordFileDoesNotExist:
            print(colored(f"{self.obj_.x_mark_} DB not found. Try adding a password {self.obj_.x_mark_}", "red"))
            return await self.begin()


    async def list_passwords(self):
        """Lists all websites stored in DB
        """
        return self.obj_.list_passwords(self.filename_)

        


    async def delete_password(self):
        """Deletes a single password from DB
        
        Raises:
            UserExits: User exits
        """

        website = simulate_input("What website do you want to delete? (ex. google.com): ").strip()

        try:
            self.obj_.delete_password(self.filename_, website)
            await alert_frontend("Successfully Deleted!")
            return await self.begin()
        except:
            await alert_frontend("An Error occured...")
            await self.begin()

    async def delete_all_data(self, stored_master):
        """Deletes ALL data including master password and passwords stored. Asks for user confirmation.
        
        Arguments:
            stored_master {str} -- Master password that is stored
        
        Raises:
            UserExits: User enters exit
            MasterPasswordIncorrect: Master Passwords do not match
        """

        entered_master = simulate_input("Enter your master password to delete all stored passwords: ")

        try:
            self.obj_.delete_all_data(self.filename_, self.master_file_, stored_master, entered_master)
            await alert_frontend("reset")
            sys.exit()

        except MasterPasswordIncorrect:
            await alert_frontend("Master Password Incorrect")
