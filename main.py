

import os
import json
import pandas as pd


class Password_Manager:
    def __init__(self , Username, Password):

        #FileName to store Data
        self.fileName = "dataBase.json"
        self.user_record = None

        self.userName = Username
        self.pass_1 = Password
    
    def User_Data(self):
        with open(self.fileName , "r") as f:
            self.user_record = json.load(f)
            return self.user_record
        
    def User_Entry(self):
            with open("entries.json", "r") as f:
                data = json.load(f) 
            return data 
    

    #Function to create account --> 1
    def Create_Account(self):

        #Inputs for Username & Password
        self.user_record = None
        self.userName = (input("Create a Username : "))
        self.pass_1 = (input("Create a Master Password : "))
        pass_2 = (input("Confirm Master Password : "))


        # Checks if Password and Confirm Password Matches
        if self.pass_1 != pass_2:
            print("Password doesn't Match . Try again...")
            return
        
        #Data Format to Store in json file
        data = {
            "Username" : self.userName,
            "Password" :self.pass_1,
        }
        

        #Checks if File exists and is greater than 0 bytes
        try:
            if os.path.exists(self.fileName) and os.path.getsize(self.fileName) > 0:
                #Function to load Data
                self.user_record = self.User_Data()

        except FileNotFoundError:
            self.user_record = None
            
        #Checks if Username already exists in database
        if self.user_record and self.user_record.get("Username") == self.userName:
            print("Username Already Exists . Select Another One & Try Again....")

        else:
            with open(self.fileName , "w") as f:
                json.dump(data , f , indent=4)
            
            print("Account Created Successfully")


    #Function to create entry --> 2
    def Add_Entry(self):
        if os.path.exists(self.fileName):
            get_pass = input("Enter Master Password : ")
            user_record = self.User_Data()
            
            if get_pass == user_record.get("Password"):
                name_entry = input("Entry Name to Save(eg . Gmail) : ").lower()
                username_entry = input("Username to Save : ")
                password_entry = input("Password to Save : ")

                entries = {
                    "name_entry" : name_entry,
                    "username_entry" : username_entry,
                    "password_entry" : password_entry,
                }

                    # Check if file exists & has valid JSON(READ JSON FILE)
                if os.path.exists("entries.json") and os.path.getsize("entries.json") > 0:
                        data = self.User_Entry()
                else:
                    data = {"entries": []}   # create base structure if file empty


# Step 2: Check for existing entry
                for entry in data["entries"]:
                    if entry["name_entry"] == name_entry:
                        modify_entry = input("Entry already exists. Do you want to modify it? (Y/N): ").lower()

                        if modify_entry == "y":
                            new_username = input("New Username : ")
                            new_password = input("New Password : ")

                            entry["username_entry"] = new_username
                            entry["password_entry"] = new_password

                            with open("entries.json", "w") as f:
                                json.dump(data, f, indent=4)
                                print("Username & Password Updated Successfully...")

                        elif modify_entry == "n":
                            print("No changes made.")
                        break
                else:
                    # If not found, append new one
                    data["entries"].append(entries)
                    with open("entries.json", "w") as f:
                        json.dump(data, f, indent=4)
                    print("New entry added successfully.")

            else:
                print("Incorrect Password , Try again...")
        else:
            return ""

    # Function to remove entry --> 3
    def Remove_Entry(self):
        if os.path.exists("entries.json") and os.path.getsize("entries.json") > 0:
            get_pass = input("Enter Master Password : ")
            user_record = self.User_Data()
            
            if get_pass == user_record.get("Password"):
                entry_to_del = input("Entry name to Delete: ").strip().lower()

                # Read JSON data
                data = self.User_Entry()

                # Check if entry exists
                exists = any([item["name_entry"] == entry_to_del for item in data["entries"]])

                if not exists:
                    print("Entry name not valid , Try again...")
                else:
                    # Delete the entry
                    data["entries"] = [item for item in data["entries"] if item["name_entry"].lower() != entry_to_del]

                    # Update JSON file
                    with open("entries.json", "w") as f:
                        json.dump(data, f, indent=4)

                    print("Entry Deleted Successfully...")

            else:
                print("Incorrect Password , Try again...")

        
        else :
            print("Failed to do action...")
            return " "

    #Function to show all entries --> 4
    def Show_Entry(self):
        if os.path.exists("entries.json") and os.path.getsize("entries.json") > 0:
            get_pass = input("Enter Master Password : ")
            user_record = self.User_Data()
            
            if get_pass == user_record.get("Password"):
                data = self.User_Entry()

                df = pd.DataFrame(data["entries"])
                df.columns = ["Entry Name" , "Username" , "Password"]
                print("\n" + df.to_string(index=False))
            else:
                print("Incorrect Password , Try again...")

        else:
            return " "
        
    #Function reset Username and Password -- 5
    def Reset_Login(self):
        if os.path.exists(self.fileName) and os.path.getsize(self.fileName) > 0:
            get_pass = input("Enter Master Password : ")
            user_record = self.User_Data()
            
            if get_pass == user_record.get("Password"):
                choice = input("What to Update Username or Password (U / P): ").strip().lower()

                if choice.startswith("u"):
                    updated_username = input("Enter New Username : ")
                    data = self.User_Data()
                    data["Username"] = updated_username
                    with open(self.fileName , "w") as f:
                        json.dump(data , f , indent=4)
                    print("Username Updated Successfully...")

                elif choice.startswith("p"):
                    updated_password = input("Enter New Password : ")
                    data = self.User_Data()
                    data["Password"] = updated_password
                    with open(self.fileName , "w") as f:
                        json.dump(data , f , indent=4)
                    print("Password Updated Successfully...")
                else:
                    print("Failed to process the request , Try again...")

            else:
                print("Incorrect Password , Try again...")
        else:
            return ""   

    #Function to create menu --> 6
def menu():
      return """
Password Saver - choose an option:
1) Create Account.
2) Add entry.
3) Get entry.
4) Delete entry.
5) change login username and password.
6) quit
                """

if __name__ == "__main__":
    pm = Password_Manager(None , None)
    while True:
        print(menu())

        choice = input("Enter Choice : ").strip()

        if choice == "1":
            pm.Create_Account()

        if choice == "2":
            pm.Add_Entry()

        if choice == "3":
            pm.Show_Entry()

        if choice == "4":
            pm.Remove_Entry()

        if choice == "5":
            pm.Reset_Login()

        if choice == "6":
            print("Goodbye...")
            break