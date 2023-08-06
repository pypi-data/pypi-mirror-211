import sqlite3
from colorama import Fore, init
import datetime
init(autoreset=True)
red = Fore.RED
green = Fore.GREEN
import os.path
from hashlib import sha256 as SHA256

def sha256(data):
    return SHA256(data.encode('utf-8')).hexdigest()


def connectDB(fname):
    return sqlite3.connect(fname)

def init_error():
    raise Exception("""Librarycubed was not properly initialized
Please delete 'bcList.sqlite3' if it exists
Then run 'init_list()' in your python file.""")

def init_list():
    if os.path.isfile('bcList.sqlite3'):
        raise Exception("Blockchain List already initialized")
    else:
        conn = connectDB('bcList.sqlite3')
        c = conn.cursor()
        c.execute("CREATE TABLE list ('id' INTEGER PRIMARY KEY, 'name' text, 'fname' text)")
        conn.commit()
        conn.close()
        print(f"{green}Initialized succesfully")

def is_init():
    if os.path.isfile('bcList.sqlite3'):
        conn = connectDB('bcList.sqlite3')
        c = conn.cursor()
        c.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='list'")

        if c.fetchall() == []:
            return False
        else:
            return True
    else:
        return False

def is_file(fname):
    conn = connectDB("bcList.sqlite3")
    c = conn.cursor()
    c.execute(f"SELECT fname FROM list WHERE fname = '{fname}'")
    
    if c.fetchall() == []:
        return False
    else:
        return True

def file_error(fname):
    raise FileNotFoundError(f"file '{fname}' was not found in Blockchain List")

class Admin():
    def warning():
        print("""THE USERNAMES AND PASSWORDS OF ANY ADMIN (MASTER OR NOT) CANNOT BE ACCESSED LATER
STORE OR WRITE THEM DOWN SOMEWHERE SECURE
DO NOT SHARE ANY USERNAMES OR PASSWORDS (ESPECIALLY THOSE OF THE MASTER ADMIN) TO NON-EMPLOYEES OR UNAUTHORIZED INDIVIUALS""")

    def new(fname):
        if not is_init():
            init_error()
        elif not is_file(fname):
            file_error(fname)
        else:
            print("New admin initalization:")
            username = input("Please enter the username >> ")
            password = input("Please enter the password >> ")

            conn = connectDB(fname)
            c = conn.cursor()
            c.execute(f"SELECT * FROM admin WHERE username = '{username}' OR password = '{password}'")
            
            if c.fetchall() != []:
                raise Exception("Username or password already in use")
            else:
                conn.close()
                Admin.Master.verify(fname)

                Admin.warning()
                confirm = input("Confirm? (Y/n) >> ").lower()

                if confirm in ['n','no']:
                    raise Exception("Cancelled")
                elif confirm in ['y','yes']:
                    conn = connectDB(fname)
                    c = conn.cursor()
                    c.execute(f"INSERT INTO admin VALUES(null, '{username}', '{password}')")
                    conn.commit()
                    conn.close()
                    print(f"{green}Admin initalization successful")
                else:
                    raise Exception("Invalid response")

    def login(fname):
        if not is_init():
            init_error()
        elif not is_file(fname):
            file_error(fname)
        else:
            print("Verification:")
            username = input("Please enter your username >> ")
            password = input("Please enter your password >> ")

            conn = connectDB(fname)
            c = conn.cursor()
            c.execute(f"SELECT username, password FROM admin WHERE username = '{username}' AND password = '{password}'")
            
            if c.fetchall() == []:
                raise Exception("Invalid username or password")
            else:
                print(f"{green}Authentication succesful")
                return username

    class Master():
        def new(fname):
            if not is_init():
                init_error()
            elif not is_file(fname):
                file_error(fname)
            else:
                conn = connectDB(fname)
                c = conn.cursor()
                c.execute("SELECT * FROM admin")
                if c.fetchall() != []:
                    raise Exception("""Master Admin already initalized
To create a new admin use 'Admin.new('filename')'""")
                else:
                    print("Master Admin initalization:")
                    username = input("Please enter the username >> ")
                    password = input("Please enter the password >> ")

                    conn = connectDB(fname)
                    c = conn.cursor()
                    c.execute(f"SELECT * FROM admin WHERE username = '{username}' OR password = '{password}'")
                    
                    if c.fetchall() != []:
                        raise Exception("Username or password already in use")
                    else:
                        conn.close()

                        Admin.warning()
                        confirm = input("Confirm? (Y/n) >> ").lower()

                        if confirm in ['n','no']:
                            raise Exception("Cancelled")
                        elif confirm in ['y','yes']:
                            conn = connectDB(fname)
                            c = conn.cursor()
                            c.execute(f"INSERT INTO admin VALUES(null, '{username}', '{password}')")
                            conn.commit()
                            conn.close()
                            print(f"{green}Master Admin initalization successful")
                        else:
                            raise Exception("Invalid response")
                
        def verify(fname):
            if not is_init():
                init_error()
            elif not is_file(fname):
                file_error(fname)
            else:
                print("Verification:")
                username = input("Please enter the Master Admin username >> ")
                password = input("Please enter the Master Admin password >> ")

                conn = connectDB(fname)
                c = conn.cursor()
                c.execute("SELECT username, password FROM admin WHERE id = '1'")
                fetched = c.fetchall()

                try:
                    if username == fetched[0][0] and password == fetched[0][1]:
                        print(f"{green}Authentication succesful")
                    else:
                        raise Exception("Password or username incorrect")
                except IndexError:
                    raise Exception("""Master Admin not initalized
Please run 'Admin.Master.new(filename)'""")
                
class Blockchain():
    def new(fname, name):
        if not is_init():
            init_error()
        else:
            if fname[-8:] != '.sqlite3':
                raise Exception("filename must end with .sqlite3")
            elif fname == "bcList.sqlite3":
                raise Exception("filename cannot be 'bcList.sqlite3'")
            else:
                conn = connectDB("bcList.sqlite3")
                c = conn.cursor()
                c.execute("SELECT name, fname FROM list")
                
                for db in c.fetchall():
                    if db[0] == name:
                        raise Exception(f"name '{name}' already in use")
                    elif db[1] == fname:
                        raise Exception(f"filename '{fname}' already in use")
                else:
                    c.execute(f"INSERT INTO list VALUES(null, '{name}','{fname}')")
                    conn.commit()
                    conn.close()

                    conn = connectDB(fname)
                    c = conn.cursor()
                    c.execute("CREATE TABLE blockchain ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'borrower' text, 'book' text, 'returnBy' text, 'type' text, 'timeOfAction' text,'hash' text, 'prev_hash' text, 'timestamp' text, 'verifier' text)")
                    c.execute("CREATE TABLE pending ('borrower' text, 'book' text, 'returnBy' text, 'type' text, 'timestamp' text)")
                    c.execute("CREATE TABLE admin ('id' INTEGER PRIMARY KEY AUTOINCREMENT, 'username' text, 'password' text)")
    
                    timestamp = str(datetime.datetime.now())

                    c.execute(f"INSERT INTO blockchain VALUES(null, null, null, null, null, '{timestamp}','hash', null, '{timestamp}' ,null)")
                    
                    c.execute("SELECT * FROM blockchain")

                    hash = ""
                    for item in c.fetchall()[0]:
                        if item in ["hash", 1] :
                            pass
                        else:
                            hash += str(item)
                    hash = sha256(hash)

                    c.execute(f"UPDATE blockchain SET hash = '{hash}' WHERE id = 1;")
                    conn.commit()
                    conn.close()
                    print(f"{green}Blockchain initalized successfully!")

    def delete(fname):
        if not is_init():
            init_error()
        elif fname == 'bcList.sqlite3':
            raise Exception("Cannot delete 'bcList.sqlite3'")
        else:
            if not is_file(fname):
                file_error(fname)
            else:
                conn = connectDB("bcList.sqlite3")
                c = conn.cursor()

                c.execute(f"DELETE from list WHERE fname = '{fname}'")
                os.remove(f"{fname}")

                print(f"{green}Blockchain deleted successfully!")
                conn.commit()
                conn.close()

    def insert_into(fname, data): # borrower, book, returnBy, type
        if not is_init():
            init_error()
        elif not is_file(fname):
            file_error(fname)
        elif type(data) != dict: 
            raise Exception("""Invalid data type; use dict
Try using 'format(borrower, book, return_date, type)'
'type' should be either 'return' or 'borrow' or 'cancel'""")       
        elif len(data) != 4:
            raise Exception("""Invalid data type; use dict
Try using 'format(borrower, book, return_date, type)'
'type' should be either 'return' or 'borrow' or 'cancel'""")   
        else:
            args = ['borrower','book','returnBy','type']
            for i, key in enumerate(data):
                if args[i] != key:
                    raise Exception("""Invalid data type; use dict
Try using 'format(borrower, book, return_date, type)'
'type' should be either 'return' or 'borrow' or 'cancel'""")        
                else:
                    if args[i] == 'type':
                        if data['type'] not in ['return','borrow','cancel']:
                            raise Exception("""Invalid data type; use dict
Try using 'format(borrower, book, return_date, type)'
'type' should be either 'return' or 'borrow' or 'cancel'""")   

            conn = connectDB(fname)
            c = conn.cursor()
            c.execute(f"INSERT INTO pending VALUES ('{data['borrower']}', '{data['book']}', '{data['returnBy']}', '{data['type']}', '{str(datetime.datetime.now())}')")
            conn.commit()
            conn.close()

    def getName(fname):
        if not is_init():
            init_error()
        elif not is_file(fname):
            file_error(fname)
        else:
            conn = connectDB('bcList.sqlite3')
            c = conn.cursor()
            c.execute(f"SELECT name FROM list WHERE fname = '{fname}'")
            name = c.fetchall()
            if fname == []:
                raise Exception(f"No name found with filename '{fname}'")
            else:
                return name[0][0]

    def getFname(name):
        if not is_init():
            init_error()
        else:
            conn = connectDB('bcList.sqlite3')
            c = conn.cursor()
            c.execute(f"SELECT fname FROM list WHERE name = '{name}'")
            fname = c.fetchall()
            if fname == []:
                raise Exception(f"No file found with name '{name}'")
            else:
                return fname[0][0]

def format(borrower, book, type, returnBy = None):
    return {"borrower":borrower,"book":book,"returnBy":returnBy,"type":type}

class GetData():
    def chains():
        conn = connectDB('bcList.sqlite3')
        c = conn.cursor()
        c.execute(f"SELECT * FROM list")

        cols = [description[0] for description in c.description]
        print(cols)
        for block in c.fetchall():
            print(block)

    def chain(fname, db_type):
        db_type = db_type.lower()
        if not is_init():
            init_error()
        elif not is_file(fname):
            file_error(fname)
        elif db_type not in ['admin','pending','blockchain']:
            raise Exception("""Invalid db type given
Please use 'pending' to list unverified blocks
or 'blockchain' to see the entire blockchain
or 'admin' to see the list of admins""")
        else:
            conn = connectDB(fname)
            c = conn.cursor()
            c.execute(f"SELECT * FROM {db_type}")
            
            cols = [description[0] for description in c.description]
            print(cols)
            for block in c.fetchall():
                print(block)

    def block(fname, db_type, index):
        db_type = db_type.lower()
        if not is_init():
            init_error()
        elif not is_file(fname):
            file_error(fname)
        elif db_type not in ['admin','pending','blockchain']:
            raise Exception("""Invalid db type given
Please use 'pending' to list unverified blocks
or 'blockchain' to see the entire blockchain
or 'admin' to see the list of admins""")
        else:
            conn = connectDB(fname)
            c = conn.cursor()
            c.execute(f"SELECT * FROM {db_type}")
            
            try:
                block = c.fetchall()[index-1]
            except IndexError:
                raise Exception(f"""Block #{index-1} was not found
Note that block #1 is not at index 0, it is at index 1""")
            cols = [description[0] for description in c.description]
            print(cols)
            print(block)

def PoA(fname):
    if not is_init():
        init_error()
    elif not is_file(fname):
        file_error(fname)
    else:
        conn = connectDB(fname)
        c = conn.cursor()
        c.execute("SELECT * FROM pending ORDER BY ROWID ASC LIMIT 1")
        
        block = c.fetchall()

        if block == []:
            raise Exception("No block to verify")
        else:

            cols = [description[0] for description in c.description]
            print(cols)
            print(block)

            response = input("Is this item valid? Check carefully (Y/n) >> ").lower()
            if response in ['y','yes']:
                username = Admin.login(fname)

                conn = connectDB(fname)
                c = conn.cursor()

                data = block[0]
                c.execute("SELECT hash FROM blockchain ORDER BY id DESC LIMIT 1")

                prev_hash = c.fetchall()[0][0]

                hash = ""
                timestamp = datetime.datetime.now()
                block[0] += (prev_hash, timestamp, username)
                for item in block[0]:
                    if item == "hash":
                        pass
                    else:
                        hash += str(item)
                print(hash)
                hash = sha256(hash)

                c.execute(f"INSERT INTO blockchain VALUES (null, '{data[0]}', '{data[1]}', '{data[2]}', '{data[3]}', '{data[4]}' ,'{hash}', '{prev_hash}', '{timestamp}', '{username}')")
                c.execute(f"Delete from pending where rowid IN (Select rowid from pending limit 1);")
                conn.commit()
                conn.close()

                print(f"{green}Block successfully verified")
            elif response in ['n','no']:
                conn = connectDB(fname)
                c = conn.cursor()
                c.execute(f"Delete from pending where rowid IN (Select rowid from pending limit 1);")
                conn.commit()
                conn.close()
                print(f"{green}Block removed succesfully")
            else:
                raise Exception("Invalid response")

class Check():
    def hashes(fname):
        if not is_init():
            init_error()
        elif not is_file(fname):
            file_error(fname)
        else:
            conn = connectDB(fname)
            c = conn.cursor()

            c.execute("SELECT * FROM blockchain")
            data = c.fetchall()
            hashes = [x[6] for x in data]
            prev_hashes = [x[7] for x in data][1:]
            
            invalid = False
            for i, (h, p) in enumerate(zip(hashes, prev_hashes)):
                strData = ""
                count = -1
                for item in data[i]:
                    count += 1
                    if count in [0, 6]:
                        pass
                    else:
                        strData += str(item)
                
                if sha256(strData) == h:
                    pass
                else:
                    invalid = True
                    if h == p:
                        print(f"According to block {i+2}:")
                        print(f"Block {i+1} hash: {p}")
                        print(f"Actual Block {i+1} hashed data: {sha256(strData)}")
                    else:
                        print(f"According to block {i+2}:")
                        print(f"Block {i+1} hash: {p}")
                        print(f"Actual Block {i+1} hash: {h}")
                        print(f"{red}Data and prev hash data may have been modified\n")

            if invalid:
                print(f"{red}Invalid blocks detected, view above")
            else:
                print(f"{green}All hashes valid")

    def returns(fname):
        if not is_init():
            init_error()
        elif not is_file(fname):
            file_error(fname)
        else:
            conn = connectDB(fname)
            c  = conn.cursor()
            c.execute("SELECT borrower, book, returnBy, type FROM blockchain")
            data = c.fetchall()[1:]
            date = datetime.datetime.strftime(datetime.date.today(), "%m/%d/%Y")

            overdue = [x for x in data if x[2] <= date]
            print("User, Book, Due Date")
            for x in overdue:
                print(x[:3])
