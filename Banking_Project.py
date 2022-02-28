# Banking System Mini Project
# Robert Jones
# 2.14.2022

import logging
import bank
import datetime

logging.basicConfig(filename="logfile.log", level=logging.DEBUG)
LOGGING = logging.getLogger()

class Welcome():

    def __init__(self):
        '''Initialize name, age, and pin for user

        Raises:
            ValueError if not positive int for age and pin
            '''
        
        print("========== Welcome To Robert's Bank ==========")
        self.name = input(str("Enter your name: "))

        try:
            self.age = int(input("Enter your age: "))
            self.pin = int(input("Enter your pin: "))

        except:
            LOGGING.error("Error at {}".format(datetime.datetime.now()),exc_info=1)
            print("#### Enter a positive integer #####")
            Welcome()

        customer = bank.Bank(self.name,self.age,self.pin)
            

        run = True
        while run:
            print("************************************************************")
            print("========== 1. View Details and Balance ============")
            print("========== 2. Withdraw Money ============")
            print("========== 3. Deposit Money ============")
            print("========== 4. Quit ============")
            print("************************************************************")

            try:

                x = int(input("Enter a number from the selections above: "))
            
                if x == 1:
                    customer.view_balance()
                if x == 2:
                    customer.withdraw()
                if x == 3:
                    customer.deposit()
                if x == 4:
                    print("Thank you")
                    run = False
                elif x == 0 or x > 4:
                    print("Enter a number 1 - 4")

            except ValueError as e:
                LOGGING.error("Error at {}".format(datetime.datetime.now()),exc_info=1)
                print(e,"Enter a positive integer")

Welcome()





