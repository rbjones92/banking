# Robert Jones
# 3.17.22
# Made to access the main Banking program. 

import Banking

self = Banking.Banking()

class Begin():

    def initialization():
        print("************************")
        print("Welcome to Robert's Bank")
        print("************************")
        new_user = str(input("Are you a new user?: Y/N: "))
    
        if new_user == 'Y':
            self.create_user()
        if new_user == 'N':
            user_id = str(input("What is your user ID?: "))
            self.check_user(user_id)
            

Begin.initialization()