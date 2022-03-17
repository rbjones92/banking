# Robert Jones
# 3.17.22
# Banking OOP mini-project

import random
import logging
import sys
import datetime
import sqlalchemy
from sqlalchemy import desc, insert, select, and_

logging.basicConfig(filename="logfile.log", level=logging.DEBUG)
LOGGING = logging.getLogger()


class Banking():

    def __init__(self):
        '''
        Constructor for banking object. Creates the SQL connection and tables.
        '''
        self.engine = sqlalchemy.create_engine('mysql+pymysql://root:Ss451608!@127.0.0.1/banking_data')
        self.connection = self.engine.connect()
        self.meta = sqlalchemy.MetaData()
        self.meta.reflect(self.engine,extend_existing=True)

        self.users_table = sqlalchemy.Table(
            'user_table',self.meta,
            sqlalchemy.Column('name',sqlalchemy.String(50)),
            sqlalchemy.Column('pin',sqlalchemy.Integer()),
            sqlalchemy.Column('id',sqlalchemy.String(7)),
            extend_existing=True
        )

        self.transaction_tables = sqlalchemy.Table(
            'transaction_table',self.meta,
            sqlalchemy.Column('id',sqlalchemy.String(7)),
            sqlalchemy.Column('withdrawl',sqlalchemy.Float()),
            sqlalchemy.Column('deposit',sqlalchemy.Float()),
            sqlalchemy.Column('balance',sqlalchemy.Integer()),
            sqlalchemy.Column('time',sqlalchemy.DateTime()),
            extend_existing=True
        )


    def create_user(self):

        users_table = self.users_table

        try: 
            name = str(input('Enter your name: '))
            pin = int(input('Enter your pin: '))
            id = random.randint(1000,9999)
            user_id = name[0:3]+str(id)
            print('Your user ID is: ' , user_id)
        except:
            LOGGING.error("Error at {}".format(datetime.datetime.now()),exc_info=1)
            print("Error: Name must be string, pin must be integer")
            self.create_user()

        insert_stmt = insert(users_table).values(name=name,pin=pin,id=user_id)
        self.connection.execute(insert_stmt)
        transactions_table = self.transaction_tables
        insert_stmt = insert(transactions_table).values(id=user_id,withdrawl=0.0,deposit=0.0,balance=0.0,time=datetime.datetime.now())
        self.connection.execute(insert_stmt)

        trans = str(input('Would you like to make a transaction?: Y/N: '))
        if trans == 'Y':
            self.transaction(user_id)
        elif trans =='N':
            return



    def transaction(self,user_id):
        
        x = True
        
        while x:

            transactions_table = self.transaction_tables
            stmt = select([transactions_table]).order_by(desc(transactions_table.columns.time))
            rev_stmt = stmt.where(and_(transactions_table.columns.id == user_id))
            result = self.connection.execute(rev_stmt).first()
            balance = result[3]
            print("Account balance : ${:0.2f}".format(balance))

            dep_or_withdrawl = str(input('Deposit or withdrawl?: D/W: '))
            if dep_or_withdrawl == 'D':
                new_bal = self.deposit(balance)
                insert_stmt = insert(transactions_table).values(id=user_id,withdrawl=0.0,deposit=new_bal[0],balance=new_bal[1],time=datetime.datetime.now())
                self.connection.execute(insert_stmt)          
            if dep_or_withdrawl == 'W':
                new_bal = self.withdraw(balance)
                insert_stmt = insert(transactions_table).values(id=user_id,withdrawl=new_bal[0],balance=new_bal[1],deposit=0.0,time=datetime.datetime.now())
                self.connection.execute(insert_stmt)
            
            elif dep_or_withdrawl is not 'D' and dep_or_withdrawl is not 'W':
                print('Enter D or W')

            trans = str(input('Another transaction?: Y/N '))
            if trans == 'Y':
                continue
            if trans =='N':
                sys.exit()


    def deposit(self,balance):
        try:
            deposit_val = int(input("How much would you like to deposit?: "))
            if deposit_val > 0:
                balance = balance + deposit_val
                print("Account balance has been updated: ${:0.2f}".format(balance))
            elif deposit_val <= 0:
                raise ValueError
        except ValueError as e:
            LOGGING.error("Error at {}".format(datetime.datetime.now()),exc_info=1)
            print(e,"Enter a positive integer")
            self.deposit(balance)

        except:
            LOGGING.error("Error at {}".format(datetime.datetime.now()),exc_info=1)
            print("Enter a positive integer")
            self.deposit(balance)

        return [deposit_val,balance]
        

    def withdraw(self,balance):
        '''Withdraws int or float from balance. Must be greater than balance.
        
        Raises:
            ValueError if not positive int or float
            '''
        try:
            withdrawl = int(input('How much would you like to withdraw?: '))

            if withdrawl < 0:
                raise ValueError
                
            if balance >= withdrawl:
                print("Current balance = $",balance)
                balance = balance - withdrawl           
                print("$", withdrawl, "has been withdrawn") 
                print("Account balance has been updated: ${:0.2f}".format(balance))

            else:
                print("Withdraw failed")
                print("Insufficient Funds | Balance Available: ${:0.2f}".format(balance))
                self.withdraw(balance)

        except ValueError as e:
            LOGGING.error("Error at {}".format(datetime.datetime.now()),exc_info=1)
            print(e, "Enter a positive integer")
            self.withdraw(balance)

        return [withdrawl,balance]



    def check_user(self,user_id):

        users_table = self.users_table
        stmt = select([users_table])
        rev_stmt = stmt.where(users_table.columns.id == user_id)
        result = self.connection.execute(rev_stmt).first()

        try:
            name = result[0]
            test_id = result[2]
            print('Welcome back: ', name)


            run = True
            while run:
                if user_id == test_id:
                    print("************************************************************")
                    print("========== 1. View Details and Balance ============")
                    print("========== 2. Make Transaction ============")
                    print("========== 3. Quit ============")
                    print("************************************************************")

                    x = int(input("Enter a number from the selections above: "))

                    if x == 1:
                        self.get_balance(user_id)
                    if x == 2:
                        self.transaction(user_id)
                    if x == 3:
                        print('Thank you')
                        run = False
                        sys.exit

        except TypeError:
            print('User', user_id, 'not found')
            new = str(input('Are you a new user?: Y/N: '))
            if new == 'Y':
                self.create_user()
            elif new == 'N':
                user_id = str(input("What is your user ID?: "))
                self.check_user(user_id)
            else:
                sys.exit

    def get_balance(self,user_id):

        transactions_table = self.transaction_tables
        stmt = select([transactions_table]).order_by(desc(transactions_table.columns.time))
        rev_stmt = stmt.where(and_(transactions_table.columns.id == user_id))
        result = self.connection.execute(rev_stmt).first()
        balance = result[3]
        print("Account balance : ${:0.2f}".format(balance))