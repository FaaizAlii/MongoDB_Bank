import pymongo
import re
import os
from bson.objectid import ObjectId
import time

client = pymongo.MongoClient("mongodb+srv://faaiz:1400@cluster0.jswnxzj.mongodb.net/?retryWrites=true&w=majority")

db = client["Testdb"]

collection = db["users"]

class User:
    def create_account(self):
        name: str = input("Enter Your name: ")
        father_name: str = input("Enter Your fathers' name: ")
        age = int(input("Enter your age: "))
        password: str = self.pass_check()
        amount: int = int(input("Enter initial cash: "))
        data =  {'Name': name,
                'Father name': father_name,
                'Age': age,
                'Password': password,
                'Amount': amount
                }
        collection.insert_one(data)
        return data
    
    @staticmethod
    def pass_check():
        pattern = re.compile("(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*.])(?=.*[0-9])")
        while True:
            password = input("Enter Password: ")
            ok = re.search(pattern, password)
            if len(password) >= 8:
                if ok:
                    return password
                else:
                    print("\nPassword should contain at least:\n1 special character\n1 number!\n1 uppercase letter\n"
                          "1 lowercase letter\n")
            else:
                print("\nPassword length less then 8 characters\n")


if __name__=="__main__":
    main_switch = True
    while main_switch:
        os.system("clear")
        print("Press 1 to create an account")
        print("Press 2 to login to an account")
        print("Press 3 to show all users - ADMIN")
        print("Press 0 to exit...\n")
        inp = input("Choose: ")

        if inp == '1':
            user = User()
            data = user.create_account()
            os.system('clear')
            for key , value in data.items():
                print(key , ":" , value)
            input("\nPress Enter key to continue...\n")
            os.system('clear')

        elif inp == '2':
            login_switch = True
            id = input("Enter ID: ")
            user_id = ObjectId(id)
            password = input("Enter Password: ")
            user = collection.find_one({"_id": user_id, 'Password': password})

            if user:
                while login_switch:
                    os.system("clear")
                    print("Press 1 to Deposit Money")
                    print("Press 2 to Withdraw Money")
                    print("Press 3 to Tansfer Money")
                    print("Press 4 to show account info.")
                    print("Press 5 to close account permanently")
                    print("Press 0 to log out")
                    inp = input("\nChoose: ")
                    if inp == '0':
                        break

                    elif inp == '1':
                        cash = int(input("Enter Amount to Deposit: "))
                        new_amount = cash + user["Amount"]
                        change = {"$set" : {"Amount": new_amount}}
                        collection.update_one(user, change)
                        user = collection.find_one({"_id": user_id})
                        print("Desposit Successful!!!")
                        time.sleep(2)
                        os.system("clear")

                    elif inp == '2':
                        cash = int(input("Enter Amount to Withdraw: "))
                        if user['Amount'] >= cash:
                            new_amount = user["Amount"] - cash
                            change = {"$set" : {"Amount": new_amount}}
                            collection.update_one(user, change)
                            user = collection.find_one({"_id": user_id})
                            print("Withdraw Successful!!!")
                            time.sleep(2)
                            os.system("clear")
                        else:
                            print("Insufficient balance!!!")
                            time.sleep(2)

                    elif inp == '3':
                        print("your Current Balance : {}".format(user["Amount"]))
                        cash = int(input("Enter amount to transfer: "))
                        if user['Amount'] >= cash:
                            rec = input("Enter receiver id: ")
                            user2 = collection.find_one({"_id": ObjectId(rec)})
                            if user2:
                                collection.update_one(user, {"$set" : {"Amount" : user["Amount"] - cash}})
                                collection.update_one(user2, {"$set" : {"Amount" : user2["Amount"] + cash}})
                                print("Transfer Successfull")
                                user = collection.find_one({"_id" : user_id})
                                print("Your New Balance is : {}".format(user["Amount"]))
                                time.sleep(3)
                            else:
                                print("Receiver Account Not Found!!")
                                time.sleep(2)
                        else:
                            print("Insufficient Balance!!!")
                            time.sleep(2)

                    elif inp == '4':
                        os.system("clear")
                        for key , value in user.items():
                            print(key , ":" , value)
                        input("\nEnter to Continue...\n")

                    elif inp == '5':
                        if collection.delete_one(user):
                            print("Account Closed Successfuly!!\n")
                            time.sleep(2)
                            os.system("clear")
                            break
                        else:
                            print("Error Occured!!!")
            else:
                input("Incorrect Info. Try again...(press Enter to Continue)")
                os.system("clear")
                
        elif inp == '3':
            all_users = collection.find()
            for i in all_users:
                print(i)
            input("\nPress Enter key to continue...\n")
            os.system("clear")
        elif inp == '0':
            break
        else:
            print("Wrong input")
            time.sleep(2)
                