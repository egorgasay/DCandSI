from clear_screen import clear
from functions import *
from colorama import init, Fore
from colorama import Back
from colorama import Style


class Query:
    """ 
    Query generator
    """

    def base_method(self, con):
        """ 
        Query input logic
        """
        cur = con.cursor()

        def decision_func(cur):
            """ 
            Forces you to make a choice between three options
            """
            print('''
             _                                _
            | \  _. _|_  _. |_   _.  _  _    /   _  ._  _|_ ._  _  | |  _  ._   1 Type query manualy
            |_/ (_|  |_ (_| |_) (_| _> (/_   \_ (_) | |  |_ |  (_) | | (/_ |
                   __         ___                                               2 Simple query
            ()    (_   _. |    |  ._  _|_  _  ._ ._  ._  _  _|_  _  ._
            (_X   __) (_| |   _|_ | |  |_ (/_ |  |_) |  (/_  |_ (/_ |           3 Run from file
                        |                        |
            ''')
            decision = input("# ")
            if decision == str(2):
                '''
                Simple auto query
                '''
                print(f"SQL QUERY. ")
                user_columns = input(">> SELECT ")
                table_name = input(">> FROM ")
                # check the input for the presence of ALL
                if user_columns.lower() == "all":
                    user_columns = "*"
                where = i if (i := 'WHERE ' + input('>> WHERE ')
                              ) != 'WHERE ' else ''
                group_by = i if (i := 'GROUP BY ' +
                                 input('>> GROUP BY ')) != 'GROUP BY ' else ''
                having = i if (i := 'HAVING ' +
                               input('>> HAVING ')) != 'HAVING ' else ''
                order = i if (i := 'ORDER BY ' +
                              input('>> ORDER BY ')) != 'ORDER BY ' else ''
                limit = i if (i := 'LIMIT ' + input('>> LIMIT ')
                              ) != 'LIMIT ' else ''
                optionalArray = [where, group_by, having, order, limit]
                optionalArray = list(filter(None, optionalArray))
                optional = ''.join(optionalArray)
                # execute cursor
                try:
                    cur.execute(
                        f'''SELECT {user_columns} FROM {table_name} {optional}''')
                except Exception as e:
                    cur.execute("rollback")
                    input(Fore.RED + f"{e}" + Style.RESET_ALL)
                    return 0
                query_output_logic(cur.fetchall(), cur.description)
                back = input("Go back to the main menu? (n - default)")
                if 'y' in back.lower():
                    return 0
                else:
                    clear()
                    decision_func(cur)
            elif decision == str(1):
                """ 
                Сomplex query
                """
                print("SQL ")
                user_query = input("SQL >> ").strip("\n")
                create_and_execute_ready_query(user_query, con)
                return 0
            elif decision == str(3):
                file_executor(cur)
                return 0
            else:
                # TODO: сделать try except error рекурсии
                return 0
        decision_func(cur)
