from getpass import getpass
import stdiomask
import pyodbc
import psycopg2
from clear_screen import clear
import os


class ConnectDB:
    """ 
    Connect to a database
    """

    def __init__(self):
        self.con = ''

    def connec_db(self):
        try:
            # TODO: сделать обработку неполного ввода
            clear()
            print('''
             _                                _
            | \  _. _|_  _. |_   _.  _  _    /   _  ._  _|_ ._  _  | |  _  ._
            |_/ (_|  |_ (_| |_) (_| _> (/_   \_ (_) | |  |_ |  (_) | | (/_ |
                   __         ___
            ()    (_   _. |    |  ._  _|_  _  ._ ._  ._  _  _|_  _  ._
            (_X   __) (_| |   _|_ | |  |_ (/_ |  |_) |  (/_  |_ (/_ |
                        |                        |
            ''')

            empty_or_not = os.stat('info.txt')
            global info
            info = []
            empty_or_not = empty_or_not.st_size

            def read_from_non_empty_file():
                with open('info.txt', 'r') as f:
                    for line in f:
                        info.append(line[:-1])
                    return info

            def empty():
                global postgres_or_mssm
                postgres_or_mssm = input('1 PostgreSQL\n2 MS SQL Server\n# ')
                if postgres_or_mssm == '1':
                    with open('info.txt', 'w+') as f:
                        f.write('1' + '\n')
                        f.write(input("Database name: ") + '\n')
                        f.write(input("Host name: ") + '\n')
                        f.write(input("Port: ") + '\n')
                        f.write(input("User name: ") + '\n')
                elif postgres_or_mssm == '2':
                    print("1 Connection string for MS SQL Server")
                    print("2 Connection credentials for MS SQL Server")
                    global str_or_cred
                    str_or_cred = input("# ")
                    if str_or_cred == '1':
                        with open('info.txt', 'w+') as f:
                            f.write('2' + '\n')
                            f.write('1' + '\n')
                    elif str_or_cred == '2':
                        with open('info.txt', 'w+') as f:
                            f.write('2' + '\n')
                            f.write('2' + '\n')
                            f.write(input("Server: ") + '\n')
                            f.write(input("Database: ") + '\n')
                            global trusted_connection
                            trusted_connection = input(
                                "Trusted_Connection: True - default ")
                            if trusted_connection.lower() == 'false':
                                f.write('n' + '\n')
                                f.write(input("User name: ") + '\n')
                            else:
                                f.write('y' + '\n')
                    else:
                        input('Please, enter 1 or 2')
                        connec_db()
                else:
                    input('Please, enter 1 or 2')
                    connec_db()

                return read_from_non_empty_file()
            if empty_or_not == 0:
                empty()
            else:
                decision = input(
                    "Restore previous session? (Y/n): Y - default : ")
                if "n" in decision.lower():
                    info = empty()
                else:
                    info = read_from_non_empty_file()

            # print(info)
            if info[0] == '1':
                self.con = psycopg2.connect(
                    database=info[-4],
                    user=info[-1],
                    password=stdiomask.getpass(),
                    host=info[-3],
                    port=info[-2]
                )
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
                        except:
                            print("Check your credentials and try again.")
            else:
                input("Something went wrong. Please try again.")
                connec_db()
            print("Opened successfully")
            global cur
            try:
                cur = self.con.cursor()
            except:
                print("Check your credentials and try again.")
                exit(0)
            clear()
            return self.con, info, cur
        except psycopg2.OperationalError:
            print(f'Could not connect to database server. Check your credentials')
            exit(0)
        except KeyboardInterrupt:
            connec_db()
