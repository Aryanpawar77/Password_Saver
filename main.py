import os
import json
import pandas as pd


class Password_Manager:
    def __init__(self, Username, Password):
        self.dataFile = "dataBase.json"
        self.entryFile = "entries.json"
        self.user_record = None
        self.userName = Username
        self.pass_1 = Password

    # Sub Function --> 1 load json file Data
    def load_json(self, path, default):
        if os.path.exists(path) and os.path.getsize(path) > 0:
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except (json.JSONDecodeError, OSError):
                return default
        else:
            return default
    # Sub Function --> 2 to create default values for login    
    def default_value(self):
        #Read json file
        data = self.load_json(self.dataFile, {})

        #Modify Json file
        data["Username"] = "User"
        data["Password"] = None

        #Update json File
        with open(self.dataFile , 'w') as f:
            json.dump(data , f)

    #Sub Function --> 3 to check if master ACCOUNT / password is set or not
    def verify_master_account(self):
        """Check if master account and password exist and return user record."""
        # Check if file exists and not empty
        if not os.path.exists(self.dataFile) or os.path.getsize(self.dataFile) == 0:
            print("Master account not found. Create an account first.")
            return None

        # Load JSON data
        user_record = self.load_json(self.dataFile, {})

        # Check if password key missing or None/empty
        if not user_record.get("Password"):
            print("Master password not set. Please create an account first.")
            return None

        return user_record

    # Function to create account --> 1
    def Create_Account(self):
        # Inputs for Username & Password
        self.userName = input("Create a Username : ").strip()
        self.pass_1 = input("Create a Master Password : ")
        pass_2 = input("Confirm Master Password : ")

        # Checks if Password and Confirm Password Matches
        if self.pass_1 != pass_2:
            print("Password doesn't Match . Try again...")
            return

        # Data Format to Store in json file
        data = {"Username": self.userName, "Password": self.pass_1}

        # Load a json file
        user_record = self.load_json(self.dataFile, {})

        # Checks if Username already exists in database
        if user_record.get("Username") == self.userName:
            print("Username Already Exists . Select Another One & Try Again....")
            return

        # Save new account
        with open(self.dataFile, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

        print("Account Created Successfully")

    # Function to create entry --> 2
    def Add_Entry(self):
        user_record = self.verify_master_account()
        if not user_record:
            return  # Stop if verification failed

        get_pass = input("Enter Master Password : ")
        user_record = self.load_json(self.dataFile, {})

        if get_pass == user_record.get("Password"):
            name_entry = input("Entry Name to Save(eg . Gmail) : ").strip().lower()
            username_entry = input("Username to Save : ").strip()
            password_entry = input("Password to Save : ").strip()

            if not name_entry:
                print("Invalid entry name.")
                return

            entries = {
                "name_entry": name_entry,
                "username_entry": username_entry,
                "password_entry": password_entry,
            }

            # (READ JSON FILE)
            data = self.load_json(self.entryFile, {"entries": []})

            # Step 2: Check for existing entry
            for entry in data["entries"]:
                if entry.get("name_entry") == name_entry:
                    modify_entry = input(
                        "Entry already exists. Do you want to modify it? (Y/N): "
                    ).strip().lower()

                    if modify_entry == "y":
                        new_username = input("New Username : ").strip()
                        new_password = input("New Password : ").strip()

                        entry["username_entry"] = new_username
                        entry["password_entry"] = new_password

                        with open(self.entryFile, "w", encoding="utf-8") as f:
                            json.dump(data, f, indent=4)
                        print("Username & Password Updated Successfully...")
                    else:
                        print("No changes made.")
                    break
            else:
                # If not found, append new one
                data["entries"].append(entries)
                with open(self.entryFile, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                print("New entry added successfully.")

        else:
            print("Incorrect Password , Try again...")

    # Function to remove entry --> 3
    def Remove_Entry(self):
        if not os.path.exists(self.entryFile) or os.path.getsize(self.entryFile) == 0:
            print("No entries file found or file is empty.")
            return

        get_pass = input("Enter Master Password : ")
        user_record = self.load_json(self.dataFile, {})

        if get_pass == user_record.get("Password"):
            entry_to_del = input("Entry name to Delete: ").strip().lower()
            if not entry_to_del:
                print("Invalid entry name.")
                return

            # Read JSON data
            data = self.load_json(self.entryFile, {"entries": []})

            # Check if entry exists
            exists = any(item.get("name_entry") == entry_to_del for item in data["entries"])

            if not exists:
                print("Entry name not valid , Try again...")
            else:
                # Delete the entry
                data["entries"] = [
                    item for item in data["entries"] if item.get("name_entry", "").lower() != entry_to_del
                ]

                # Update JSON file
                with open(self.entryFile, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)

                print("Entry Deleted Successfully...")

        else:
            print("Incorrect Password , Try again...")

    # Function to show all entries --> 4
    def Show_Entry(self):
        if not os.path.exists(self.entryFile) or os.path.getsize(self.entryFile) == 0:
            print("No entries to show.")
            return

        get_pass = input("Enter Master Password : ")
        user_record = self.load_json(self.dataFile, {})

        if get_pass == user_record.get("Password"):
            data = self.load_json(self.entryFile, {"entries": []})

            if not data.get("entries"):
                print("No entries saved.")
                return

            df = pd.DataFrame(data["entries"])

            # Ensure dataframe has expected columns before renaming
            expected_cols = ["name_entry", "username_entry", "password_entry"]
            missing = [c for c in expected_cols if c not in df.columns]
            if missing:
                # If json entries don't have expected structure, show raw data
                print("Entries have unexpected format. Raw data:")
                print(json.dumps(data, indent=4))
                return

            df = df.rename(
                columns={
                    "name_entry": "Entry Name",
                    "username_entry": "Username",
                    "password_entry": "Password",
                }
            )
            print("\n" + df.to_string(index=False))
        else:
            print("Incorrect Password , Try again...")

    # Function reset Username and Password -- 5
    def Reset_Login(self):
        user_record = self.verify_master_account()
        if not user_record:
            return  # Stop if verification failed

        get_pass = input("Enter Master Password : ")
        user_record = self.load_json(self.dataFile, {})

        if get_pass == user_record.get("Password"):
            choice = input("What to Update Username or Password (U / P): ").strip().lower()

            if choice.startswith("u"):
                updated_username = input("Enter New Username : ").strip()
                data = self.load_json(self.dataFile, {})
                data["Username"] = updated_username
                with open(self.dataFile, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                print("Username Updated Successfully...")

            elif choice.startswith("p"):
                updated_password = input("Enter New Password : ")
                data = self.load_json(self.dataFile, {})
                data["Password"] = updated_password
                with open(self.dataFile, "w", encoding="utf-8") as f:
                    json.dump(data, f, indent=4)
                print("Password Updated Successfully...")
            else:
                print("Failed to process the request , Try again...")

        else:
            print("Incorrect Password , Try again...")


     # Function to delete account --> 6
    def Delete_Account(self):
        user_record = self.verify_master_account()
        if not user_record:
            return  # Stop if verification failed

        # Verify master password
        get_pass = input("Enter Master Password: ")
        user_record = self.load_json(self.dataFile, {})
        if get_pass != user_record.get("Password"):
            print("Incorrect Master Password.")
            return

        # Explicit confirmation
        confirm = input(
            "Type DELETE to permanently remove the account and all entries: "
        ).strip()
        if confirm != "DELETE":
            print("Cancelled. Account not deleted.")
            return

        # Attempt deletion
        errors = []
        for path in (self.dataFile, self.entryFile):
            try:
                if os.path.exists(path):
                    os.remove(path)
            except Exception as e:
                errors.append(f"{path}: {e}")

        if errors:
            print("Deletion completed with errors:")
            for e in errors:
                print(" -", e)
        else:
            print("Account and all related data have been deleted.")



# Function to create menu --> 7
    def menu(self):
        user_record = self.load_json(self.dataFile, {})
        return f"""
Password Saver (Welcome , {user_record.get("Username")})- choose an option:
1) Create Account.
2) Add entry.
3) Get entry.
4) Delete entry.
5) change login username and password.
6) Delete Account.
7) quit
                """


if __name__ == "__main__":
    pm = Password_Manager("User", None)
    pm.default_value() # to load default values
    while True:
        print(pm.menu())
        choice = input("Enter Choice : ").strip()
        if choice == "1":
            pm.Create_Account()
        elif choice == "2":
            pm.Add_Entry()
        elif choice == "3":
            pm.Show_Entry()
        elif choice == "4":
            pm.Remove_Entry()
        elif choice == "5":
            pm.Reset_Login()
        elif choice == "6":
            pm.Delete_Account()
        elif choice == "7":
            print("Goodbye...")
            break
        else:
            print("Invalid option.")
