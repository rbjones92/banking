# Banking System Mini Project
# Robert Jones
# 2.14.2022

import logging
import bank
import datetime
import sqlalchemy
from sqlalchemy.orm import sessionmaker
from sqlalchemy import insert, select, and_

logging.basicConfig(filename="logfile.log", level=logging.DEBUG)
LOGGING = logging.getLogger()

class MySql():

    def __init__(self,name,age,pin,update,balance):
        self.name = name
        self.age = age
        self.pin = pin
        self.update = update
        self.balance = balance

        engine = sqlalchemy.create_engine('mysql+pymysql://root:Ss451608!@127.0.0.1/banking_data')
        connection = engine.connect()
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        
        meta = sqlalchemy.MetaData()

        bank_table = sqlalchemy.Table(
            'bank_data_2',meta,
            sqlalchemy.Column('name',sqlalchemy.String(50)),
            sqlalchemy.Column('age',sqlalchemy.Integer()),
            sqlalchemy.Column('pin',sqlalchemy.Integer()),
            sqlalchemy.Column('withdrawl',sqlalchemy.Float()),
            sqlalchemy.Column('deposit',sqlalchemy.Float()),
            sqlalchemy.Column('balance',sqlalchemy.Float()),
        )

        
        def insert_sql():
            insert_stmt = insert(bank_table).values(name=self.name,age=self.age,pin=self.pin,balance=self.balance)
            result = connection.execute(insert_stmt)
    
        if update == True:
            insert_sql()



        def get_balance():
            stmt = select([bank_table])

            stmt = stmt.where(and_(bank_table.columns.pin == pin ,bank_table.columns.name == name))

            for result in connection.execute(stmt):
                global BALANCE 
                BALANCE = result.balance
                
        if balance == True and balance != int():
            get_balance()



MySql(name=0,age=0,pin=0,update=False,balance=False)


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
            self.balance = MySql(self.name,self.age,self.pin,update=False,balance=True)
            
        except:
            LOGGING.error("Error at {}".format(datetime.datetime.now()),exc_info=1)
            print("#### Enter a positive integer #####")
            Welcome()

        customer = bank.Bank(self.name,self.age,self.pin,BALANCE)
            

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
                    MySql(self.name,self.age,self.pin,update=True,balance=customer.get_balance())
                    run = False
                elif x == 0 or x > 4:
                    print("Enter a number 1 - 4")

            except ValueError as e:
                LOGGING.error("Error at {}".format(datetime.datetime.now()),exc_info=1)
                print(e,"Enter a positive integer")

Welcome()





