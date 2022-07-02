import psycopg2
from prettytable import PrettyTable
import random as rnd
import os
import platform
from clear_screen import clear
from getpass import getpass
import stdiomask
import pyodbc


class Query:
    ''' Query generator
    '''

    def base_method(self):
        ''' Query input logic
        '''

        def decision_func(cur):
            ''' Forces you to make a choice between two options
            '''
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
                '''simple auto query
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
                except:
                    cur.execute("rollback")
                query_output_logic(cur.fetchall(), cur.description)
                back = input("Go back to the main menu? (n - default)")
                if 'y' in back.lower():
                    main_menu()
                else:
                    clear()
                    decision_func(cur)
            elif decision == str(1):
                '''complex query
                '''
                print("SQL ")
                user_query = input("SQL >> ").strip("\n")
                create_and_execute_ready_query(user_query)
                main_menu()
            elif decision == str(3):
                file_executor()
                main_menu()
                # print("Closed successfully")
                exit(0)
            else:
                # TODO: сделать try except error рекурсии
                print("Please select 1 or 2")
                decision_func(cur)
        decision_func(cur)


class Creator:
    ''' To create tables
    '''

    def base_method(self):
        table_name = input("Table name: ")

        def create_and_fill(table_name):
            temp_data_of_columns, temp_data_of_columnsArray, count_of_columns = create_only(
                table_name)
            temp_data_of_lines = []
            count_of_lines = int(input("Count of lines: "))
            temp_data_of_linesStringStorage = ''
            temp_data_of_columnsArrayFull = temp_data_of_columns.split(', ')
            try:
                ignore_list = []
                for j in range(1, count_of_lines + 1):
                    for x in range(1, count_of_columns + 1):
                        if 'primary key' not in temp_data_of_columnsArrayFull[x - 1].lower():
                            # todo: сделать обработку неправильного ввода, например когда забыли ввести INT
                            item = input(
                                f"line:{j} item:{temp_data_of_columnsArray[x-1]} > ")
                            item = item.split()
                            item_type = type_finder(item[0])

                            def if_item_is_null(item, temp_data_of_columnsArray, temp_data_of_columnsArrayFull):
                                if 'null' in item or 'Null' in item or 'NULL' in item:
                                    # print(temp_data_of_columnsArrayFull[x - 1])
                                    if 'not null' not in temp_data_of_columnsArrayFull[x - 1].lower():
                                        # print("Test1")
                                        item = None
                                        return item
                                    print(
                                        f"item:{temp_data_of_columnsArray[x-1]} can't be null")
                                    item = input(
                                        f"line:{j} item:{temp_data_of_columnsArray[x-1]} > ")
                                    if 'null' in item.lower():
                                        return if_item_is_null(item, temp_data_of_columnsArray,
                                                               temp_data_of_columnsArrayFull)
                                    else:
                                        return item
                                else:
                                    return item
                            item = if_item_is_null(
                                item, temp_data_of_columnsArray, temp_data_of_columnsArrayFull)
                            if item_type == 'int' or item_type == 'float':
                                temp_data_of_linesStringStorage += item[0] + ', '
                            else:
                                if item is None:
                                    temp_data_of_linesStringStorage += 'NULL' + ', '
                                else:
                                    temp_data_of_linesStringStorage += '\'' + \
                                        item[0] + '\'' + ', '
                        else:
                            ignore_list.append(
                                temp_data_of_columnsArrayFull[x - 1])

                    temp_data_of_lines.append(temp_data_of_linesStringStorage)

                    temp_data_of_linesStringStorage = ''
            except Exception as e:
                print(e)
                input("Back to main menu")
                main_menu()
            try:
                ignore_list = list(set(ignore_list))
                temp_data_of_columns_ready = ''
                temp_data_of_linesStringStorage2 = ''
                for counter in range(len(ignore_list)):
                    ignore_list = (" ").join(ignore_list)
                    print(temp_data_of_columnsArray[counter], ignore_list)
                    if temp_data_of_columnsArray[counter] in ignore_list:
                        temp_data_of_columnsArray.pop(counter)
                temp_data_of_columns_ready = ", ".join(
                    temp_data_of_columnsArray)
                for j in range(count_of_lines):
                    temp_data_of_linesStringStorage2 = temp_data_of_lines[j]
                    try:
                        cur.execute(f'''INSERT INTO {table_name} ({temp_data_of_columns_ready})
                        VALUES ({temp_data_of_linesStringStorage2[:-2]})''')
                    except Exception as e:
                        cur.execute("rollback")
                        print(e)
                        input('Something went wrong while inserting lines..')
                        clear()
                        main_menu()
                con.commit()
                print("Success!")
                try:
                    cur.execute(f'''SELECT * FROM {table_name}''')
                except:
                    cur.execute("rollback")
                query_output_logic(cur.fetchall(), cur.description)
                input("Back to main menu")
                clear()
                main_menu()
            except Exception as e:
                print(e)
                input("Back to main menu")
                main_menu()

        def create_only(table_name):
            temp_data_of_columns = ''
            temp_data_of_columnsArray = []
            temp_data_of_columnsArrayFull = []
            count_of_columns = int(input("Count of columns: "))
            print("Example: ID SERIAL PRIMARY KEY")
            for i in range(1, count_of_columns + 1):
                columns = input(f"column:{i} : ")
                temp_data_of_columnsArray.append(columns.split()[0])
                temp_data_of_columnsArrayFull.append(columns.split())
                temp_data_of_columns += columns + ", "
                temp_data_of_columns = temp_data_of_columns.strip('\n')
            try:
                # FOR MYSQL in the future
                # if 'auto_increment' not in temp_data_of_columns.lower():
                cur.execute(f'''CREATE TABLE {table_name}
                ({temp_data_of_columns[:-2]})''')
                # else:
                #    cur.execute(f'''CREATE TABLE {table_name}
                #    ({temp_data_of_columns[:-2]+"PRIMARY KEY ({})"})''')
                con.commit()
                # if 'SERIAL PRIMARY KEY' in temp_data_of_columnsArrayFull:
                #     for counter in range(temp_data_of_columnsArrayFull.count("SERIAL PRIMARY KEY")):
                #         temp_data_of_columnsArrayFull.index(value)
                print("Success!")
                # if temp_data_of_columns
                input("Next")
                clear()
            except Exception as e:
                cur.execute("rollback")
                print(e)
                input('Something went wrong while creating table..')
                clear()
                main_menu()

            return temp_data_of_columns, temp_data_of_columnsArray, count_of_columns

        decision = input(
            f"Do you want to add some data in {table_name}? (Y/n) n - default :")
        if decision.lower() == 'y':
            create_and_fill(table_name)
        else:
            create_only(table_name)
            main_menu()


class Deletor:
    ''' To delete tables
    '''

    def __init__(self, table_name):
        self.table_name = table_name

    def base_method(self):
        print(
            f"Confirm deleting the {self.table_name}. Enter the database name.")
        decision = input("SQL: DROP TABLE ")
        if decision == self.table_name:
            try:
                cur.execute(f'''DROP TABLE IF EXISTS {self.table_name}''')
            except:
                cur.execute("rollback")
            con.commit()
            print(f"DROP TABLE {self.table_name} was completed successfully!")
            main_menu()
        input("The names of the tables do not match!")
        main_menu()


def create_and_execute_ready_query(user_query):
    ''' Creating and executing ready query
    '''
    cur = con.cursor()
    query, enter = '', 1
    text_of_query = [user_query]
    while user_query != 'EOF' and enter != 2:
        query += user_query + " "
        user_query = input("SQL >> ").strip("\n")
        text_of_query.append(user_query)
        if user_query == '':
            user_query = i if (i := input(
                "SQL >> ").strip("\n")) != 'EOF' else ''
            text_of_query.append(user_query)
            if user_query == '':
                enter = 2
    decision4 = input("Do you want to change the query? (Y/n) n - default: ")
    if decision4.lower() == 'y' or decision4.lower() == 'yes':
        # generate a random name of file and return ready query in .txt
        file_name = 'query_' + str(rnd.randint(0, 100000)) + '.txt'
        with open(file_name, 'w+') as f:
            for line in range(len(text_of_query)):
                f.write(text_of_query[line] + '\n')
        os.system(f"{file_name}")
        print(f"Saved in {file_name}")
        wait_until_done = input("# Waiting for your changes...(ENTER) ")
        file_executor(file_name)
        con.commit()
        main_menu()
        # print("Closed successfully")
        exit(0)
    #
    try:
        cur.execute(f'''{query}''')
    except:
        cur.execute("rollback")
        input("Back to main menu")
        clear()
        main_menu()
    con.commit()
    try:
        query_output_logic(cur.fetchall(), cur.description)
    except Exception as e:
        if 'DROP TABLE' in query.upper() and 'no results to fetch' in str(e):
            print("Deleted successfully")
        else:
            print(f"Error in query text!{e}!")
            input("Back to main menu")
            main_menu()
    save_decision = input("Save the query text? (Y/n): ")
    if save_decision.lower() == 'n' or save_decision.lower() == 'no':
        pass
    else:
        text_of_query = list(filter(None, text_of_query))
        file_name = 'query_' + str(rnd.randint(0, 100000)) + '.txt'
        with open(file_name, 'w+') as f:
            for line in range(len(text_of_query)):
                f.write(text_of_query[line] + '\n')
        input(f"Saved in {file_name}")


def type_finder(x):
    ''' Type finder
    '''
    try:
        if x == True or x == False:
            return 'bool'
        int(x)
        return 'int'
    except ValueError:
        try:
            float(x)
            return 'float'
        except ValueError:
            if x.lower().startswith('enum'):
                return 'enum'
            elif x.lower().startswith('set'):
                return 'set'
            return 'str'


def query_output_logic(rows, columns_from_cur):
    ''' Query output logic
    '''
    coulums = []  # array of columns names
    for i in range(len(columns_from_cur)):  # filling colums by cur.description
        coulums.append((columns_from_cur[i][0]).upper())

    dt = []  # empty array of elements
    for row in rows:  # filling array of elements
        for element in row:
            # deleting ussles characters from the string
            element = str(element).strip()
            dt.append(element)
    rtable = PrettyTable(coulums)  # creating table
    while dt:  # formatting table
        column = len(coulums)
        rtable.add_row(dt[:column])
        dt = dt[column:]
    clear()
    print(rtable)


def file_executor(file_name=''):
    ''' Executing a query from a file
    '''
    if file_name == '':
        file_name = input("File name or path to the file: ")
    if file_name.count("/") != 0:
        file_name.replace("/", "\\\\")
        print(file_name)
    try:
        with open(file_name, 'r') as f:
            text_of_query = []
            for line in f:
                text_of_query.append(line.strip('\n'))
    except Exception as e:
        print(f"Exception occurred while executing command. {e}")
        file_executor()
    query = ' '.join(text_of_query)
    try:
        cur.execute(f'''{query}''')
        query_output_logic(cur.fetchall(), cur.description)
    except:
        cur.execute("rollback")  # rollback if query is bad
        print("Something went wrong while executing query.")
    decision = input("Do you want to run the query again? (Y/n) y - Default: ")
    if decision.lower() == 'n' or decision.lower() == 'no':
        main_menu()
        exit(0)
    file_executor(file_name)


def connec_db():
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
            decision = input("Restore previous session? (Y/n): Y - default : ")
            if "n" in decision.lower():
                info = empty()
            else:
                info = read_from_non_empty_file()

        # print(info)
        global con
        con = ''
        if info[0] == '1':
            con = psycopg2.connect(
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
                con = pyodbc.connect(con_str)
            else:
                # true con or not
                if info[-2] == 'n':
                    # Trusted_Connection = no
                    try:
                        con = pyodbc.connect(
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
                        con = pyodbc.connect(
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
            cur = con.cursor()
        except:
            print("Check your credentials and try again.")
            exit(0)
        clear()
        return con
    except psycopg2.OperationalError:
        print(f'Could not connect to database server. Check your credentials')
        exit(0)
    except KeyboardInterrupt:
        connec_db()


connec_db()


def main_menu():
    try:
        # clear()
        # TODO: Id INT AUTO_INCREMENT

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
            command.base_method()
        elif commands == '2':
            clear()
            command = Deletor(input("Enter the name of the table: "))
            command.base_method()
        elif commands == '3':
            clear()
            command = Query()
            command.base_method()
        elif commands == '4':
            exit(0)
        else:
            create_and_execute_ready_query(commands.strip("\n"))
            main_menu()
    except Exception as e:
        print(f"Exception occurred while executing command. {e}")
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
    main_menu()
