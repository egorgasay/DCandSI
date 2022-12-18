from getpass import getpass
import stdiomask
import pyodbc
import psycopg2
from clear_screen import clear
import os
from colorama import init, Fore
from colorama import Back
from colorama import Style
from werkzeug.exceptions import abort
import hashlib
import os
import sqlite3


class ConnectDB:
    """ 
    Connect to a database
    """

    def __init__(self, con, main_username):
        self.info = None
        self.con = con
        self.cur = con.cursor()
        self.main_username = main_username

    def compare_passwords(self, username, password, cur):
        passwd_from_db = ''
        try:
            datapswd = cur.execute(
                f"""SELECT password FROM Users WHERE username = '{username}'""")
            passwd_from_db = tuple(datapswd.fetchone())
        except:
            return 'Wrong username'
        return 'OK' if password == passwd_from_db[0] else 'Wrong password'

    def encrypt_password(self, password):
        salt = os.urandom(32)
        key = password
        new_key = hashlib.pbkdf2_hmac('sha256',
                                      password.encode('utf-8'),
                                      salt,
                                      100200)
        return new_key

    def record_user_db(self, conn, hostname, bdname, username, password, port, TYPE):
        cur = conn.cursor()
        if TYPE == 'PSQL':
            try:
                cur.execute(
                    f"""INSERT INTO Data VALUES ('{self.main_username}', '{hostname}', '{bdname}', '{username}', '{password}', {port}, '{TYPE}')""")
                conn.commit()
            except Exception as e:
                print(str(e))
                cur.execute('ROLLBACK')
                conn.close()
                return 'Err'
            return 'OK'

    def create_user(self, username, password, conn):
        self.conn = conn
        cur = self.conn.cursor()
        try:
            #new_passwd = str(self.encrypt_password(password)).replace('\\', '1')[2:-2]
            # print(new_passwd)
            cur.execute(
                f"""INSERT INTO Users (username, password) VALUES ('{username}', '{password}');""")
            conn.commit()
        except Exception as e:
            if 'UNIQUE constraint failed' in str(e):
                return f'The username is already taken'
            cur.execute('ROLLBACK')
            conn.close()
            return f'Error {e}'
        return 'OK'

    def connec_db(self, conn):
        try:
            try:
                cur = conn.cursor()
                data_from_query = cur.execute(
                    f"""SELECT * FROM Data WHERE username = '{self.main_username}'""")
                data_from_query = tuple(data_from_query.fetchone())
            except Exception as e:
                print('Тут ничего нет')
                print(str(e))
                if 'NoneType' in str(e):
                    return None, self.info, None
                # abort(403)
            empty_or_not = 2 if len(data_from_query) > 0 else 0

            if empty_or_not == 0:
                return 'No data in table'
            else:
                self.info = info = data_from_query

            # print(info)
            if info[-1] == 'PSQL':
                try:
                    self.con = psycopg2.connect(
                        database=info[-5],
                        user=info[-4],
                        password=info[-3],
                        host=info[-6],
                        port=info[-2]
                    )
                except Exception as e:
                    print(str(e), 'Wrong credentials')
                    return 'Wrong credentials'
            # postgres or ms sql
            elif info[0] == '2':
                # str or cred
                if info[1] == '1':
                    con_str = input("Connection string: ")
                    self.con = pyodbc.connect(con_str)
                else:
                    # true con or not
                    if info[-2] == 'n':
                        # Trusted_Connection = no
                        try:
                            self.con = pyodbc.connect(
                                "Driver={ODBC Driver 17 for SQL Server};"
                                "Server=" + info[-3] + ";"
                                "Database=" + info[-2] + ";"
                                "User Id=" + info[-1] + ";"
                                "Password=" + stdiomask.getpass() + ";"
                            )
                        except:
                            print("Check your credentials and try again.")
                    else:
                        # Trusted_Connection = yes
                        try:
                            self.con = pyodbc.connect(
                                "Driver={ODBC Driver 17 for SQL Server};"
                                "Server=" + info[-3] + ";"
                                "Database=" + info[-2] + ";"
                                "Trusted_Connection=yes;"
                            )
                        except Exception as e:
                            print("Check your credentials and try again.")
            elif info[0] == '3':
                print("Connecting to " + info[-1])
                msa_drivers = [
                    x for x in pyodbc.drivers() if 'ACCESS' in x.upper()]
                if msa_drivers:
                    con_string = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};' \
                        rf'DBQ={info[-1]};'
                    try:
                        self.con = pyodbc.connect(con_string)
                    except Exception as e:
                        input(Fore.RED + f"{e}" + Style.RESET_ALL)
                else:
                    print(Fore.RED + "Please, install Access Driver!" +
                          Style.RESET_ALL)
                    exit(0)
            else:
                print(
                    Fore.RED + f"Something went wrong. Please try again." + Style.RESET_ALL)
                exit(0)
            print("Opened successfully")
            try:
                self.cur = self.con.cursor()
            except Exception as e:
                print(Fore.RED + f"{e}" + Style.RESET_ALL)
                exit(0)
            return self.con, self.info, self.cur
        except psycopg2.OperationalError:
            print(f'Could not connect to database server. Please, check your credentials')
            exit(0)
        except KeyboardInterrupt:
            exit(0)
