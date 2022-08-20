import os
import platform
from clear_screen import clear
from query import Query
from create import Creator
from delete import Deletor
from connect import ConnectDB
from functions import create_and_execute_ready_query
from colorama import init, Fore
from colorama import Back
from colorama import Style


def main_menu(*args):
    try:
        # clear()
        # TODO: Id INT AUTO_INCREMENT
        if args:
            global con, info, cur
            con, info, cur = [*args[0]]

        print('''
         _                                _
        | \  _. _|_  _. |_   _.  _  _    /   _  ._  _|_ ._  _  | |  _  ._  1 Create a new table
        |_/ (_|  |_ (_| |_) (_| _> (/_   \_ (_) | |  |_ |  (_) | | (/_ |   2 Delete a table
               __         ___                                              3 Execute an query
        ()    (_   _. |    |  ._  _|_  _  ._ ._  ._  _  _|_  _  ._         4 Exit
        (_X   __) (_| |   _|_ | |  |_ (/_ |  |_) |  (/_  |_ (/_ |
                    |                        |                             Or type SQL query!
        ''')
        try:
            if info[0] == '1':
                cur.execute(
                    """SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;""")
            else:
                cur.execute(
                    """SELECT name FROM sys.tables""")
            tables_names = [*(str(*i) for i in cur.fetchall())]
            print(
                f"Available tables: ", ', '.join(tables_names), ".", sep="")

        except Exception as e:
            print(e)
            print("You don't have tables in your schema! \nLet's create a new table!")
            cur.execute("rollback")
        print("Write EOF in the end of query or pres ENTER twice.")
        commands = input("SQL >> ")
        if commands == '1':
            clear()
            command = Creator()
            command.base_method(con)
            clear()
            main_menu()
        elif commands == '2':
            clear()
            command = Deletor(input("Enter the name of the table: "))
            command.base_method(con)
            clear()
            main_menu()
        elif commands == '3':
            clear()
            command = Query()
            command.base_method(con)
            clear()
            main_menu()
        elif commands == '4':
            exit(0)
        else:
            create_and_execute_ready_query(commands.strip("\n"), con)
            clear()
            main_menu()
    except Exception as e:
        input(Fore.RED + f"Exception occurred while executing command. {e}"
              + Style.RESET_ALL)
        input('Back to main menu')
        main_menu()
    except KeyboardInterrupt:
        main_menu()
    finally:
        try:
            con.close()
        except:
            print()
        clear()
        print("Closed successfully")


if __name__ == "__main__":
    con = ConnectDB()
    data = con.connec_db()
    main_menu(data)
