# Robert Jones
# Banking mini-OOP Project files
# 2.21.2022

import logging
import datetime

logging.basicConfig(filename="logfile.log", level=logging.DEBUG)
LOGGING = logging.getLogger()

class User():
    def __init__(self,name,age,pin):
        ''' Initialize a users traits'''
        self.name = name
        self.age = age
        self.pin = pin
        
    def show_details(self):
        ''' Print details to terminal'''
        print("Personal Details")
        print("Name: ", self.name)
        print("Age: ",self.age)
        print("Pin: ", self.pin)


class Bank(User):

    def __init__(self,name,age,pin):
        ''' Initialize a users traits'''
        super().__init__(name,age,pin)
        self.balance = 100

    def view_balance(self):
        '''Show balace and details of individual'''
        self.show_details()
        print("Account balance: ${:0.2f}".format(self.balance))

    def deposit(self):
        ''' Deposits int into variable balance

        Raises:
            ValueError if not positive int or float.
            '''
        try:
            deposit_val = int(input("How much would you like to deposit?: "))
            if deposit_val > 0:
                self.balance = self.balance + deposit_val
                print("Account balance has been updated: ${:0.2f}".format(self.balance))
            elif deposit_val <= 0:
                raise ValueError
        except ValueError as e:
            LOGGING.error("Error at {}".format(datetime.datetime.now()),exc_info=1)
            print(e,"Enter a positive integer")
            Bank.deposit(self) 

        except:
            LOGGING.error("Error at {}".format(datetime.datetime.now()),exc_info=1)
            print(e,"Enter a positive integer")
            Bank.deposit(self)
            

    def withdraw(self):
        '''Withdraws int or float from balance. Must be greater than balance.
        
        Raises:
            ValueError if not positive int or float
            '''
        try:
            withdrawl = int(input('How much would you like to withdraw?: '))

            if withdrawl < 0:
                raise ValueError
                
            elif self.balance >= withdrawl:
                print("Current balance = $",self.balance)
                self.balance = self.balance - withdrawl           
                print("$", withdrawl, "has been withdrawn") 
                print("Account balance has been updated: ${:0.2f}".format(self.balance))

            else:
                print("Withdraw failed")
                print("Insufficient Funds | Balance Available: ${:0.2f}".format(self.balance))
                Bank.withdraw(self)

        except ValueError as e:
            LOGGING.error("Error at {}".format(datetime.datetime.now()),exc_info=1)
            print(e, "Enter a positive integer")
            Bank.withdraw(self)
