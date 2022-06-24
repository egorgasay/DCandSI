import psycopg2
from prettytable import PrettyTable
import random as rnd
import os
import platform
from clear_screen import clear
from getpass import getpass
import stdiomask

class Status:
    status = "Not connected"

class Commands:
    table = 'table'
    def __init__(self, command):
        self.command = command
    def base_method(self, commands, con):
        cur = con.cursor()
        return cur


def file_executor(file_name=''):
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
                print (f"Exception occurred while executing command. {e}")
                file_executor()
            query =  ' '.join(text_of_query)
            try:
                cur.execute(f'''{query}''')
            except:
                cur.execute("rollback")
            query_output_logic(cur.fetchall(), cur.description)
            decision = input("Do you want to run the query again? (Y/n) y - Default: ")
            if decision.lower() == 'n' or decision.lower() == 'no':
                main_menu()
                #print("Closed successfully")
                exit(0)
            file_executor(file_name)


class Selector(Commands):
    def base_method(self, commands, con):
        ''' updates base_method from the Command module
        '''
        #cur = super().base_method(commands, con)
        #!@lru_cache

        def decision_func(cur):
            '''Forces you to make a choice between two options
            '''
            print('''
 _                                _                                 
| \  _. _|_  _. |_   _.  _  _    /   _  ._  _|_ ._  _  | |  _  ._   1 Type query manualy
|_/ (_|  |_ (_| |_) (_| _> (/_   \_ (_) | |  |_ |  (_) | | (/_ |                                                                                     
       __         ___                                               2 Simple query
()    (_   _. |    |  ._  _|_  _  ._ ._  ._  _  _|_  _  ._          
(_X   __) (_| |   _|_ | |  |_ (/_ |  |_) |  (/_  |_ (/_ |  
            |                        |                              3 Run from file
''')
            #print("Do you want to type query manualy (1) or use auto(2) query?")
            decision = input("# ")
            if decision == str(2):
                '''simple auto query
                '''
                print(f"SQL QUERY. ")
                user_columns = input(">> SELECT ")
                table_name = input(">> FROM ")
                # check the input for the presence of ALL
                if user_columns.lower() == "all": user_columns = "*"
                where = i if (i:='WHERE ' + input('>> WHERE ')) != 'WHERE ' else ''
                group_by = i if (i:='GROUP BY ' + input('>> GROUP BY ')) != 'GROUP BY ' else ''
                having = i if (i:='HAVING ' + input('>> HAVING ')) != 'HAVING ' else ''
                order = i if (i:='ORDER BY ' + input('>> ORDER BY ')) != 'ORDER BY ' else ''
                limit = i if (i:='LIMIT ' + input('>> LIMIT ')) != 'LIMIT ' else ''
                optionalArray = [where, group_by, having, order, limit]
                optionalArray = list(filter(None, optionalArray))
                optional = ''.join(optionalArray) 
                # execute cursor
                try:
                    cur.execute(f'''SELECT {user_columns} FROM {table_name} {optional}''')
                except:
                    cur.execute("rollback")
                query_output_logic(cur.fetchall(), cur.description)
                back = input("Go back to the main menu? (n - default)")
                if 'y' in back.lower():
                    main_menu()
                else:
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
        


def create_and_execute_ready_query(user_query):
    cur = con.cursor()
    query, enter = '', 1
    text_of_query = [user_query]
    while user_query != 'EOF' and enter != 2:                
        query += user_query + " "
        user_query = input("SQL >> ").strip("\n")
        text_of_query.append(user_query)
        if user_query == '':
            user_query = i if (i:=input("SQL >> ").strip("\n")) != 'EOF' else ''
            text_of_query.append(user_query)
            if user_query == '':
                enter = 2
    decision4 = input("Do you want to change the query? (Y/n) n - default: ")
    if decision4.lower() == 'y' or decision4.lower() == 'yes':                
        # generate a random name of file and return ready query in .txt
        file_name = 'query_'+str(rnd.randint(0, 100000))+'.txt'
        with open(file_name, 'w+') as f:
            for line in range(len(text_of_query)):
                f.write(text_of_query[line]+'\n')
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
    query_output_logic(cur.fetchall(), cur.description)
    save_decision = input("Save the query text? (Y/n): ")
    if save_decision.lower() == 'n' or save_decision.lower() == 'no':                
        pass
    else:
        text_of_query = list(filter(None, text_of_query))
        file_name = 'query_'+str(rnd.randint(0, 100000))+'.txt'
        with open(file_name, 'w+') as f:
            for line in range(len(text_of_query)):
                f.write(text_of_query[line]+'\n')
        input(f"Saved in {file_name}")
def type_finder(x):
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
            if x.lower().startswith('enum') :
                return 'enum'
            elif x.lower().startswith('set') :
                return 'set'
            return 'str'

class Creator(Commands):
    def base_method(self, commands, con):
        #cur = super().base_method(commands, con)
        table_name = input("Table name: ")
        def create_and_fill(table_name):
            temp_data_of_columns, temp_data_of_columnsArray, count_of_columns = create_only(table_name)
            temp_data_of_lines = []
            count_of_lines = int(input("Count of lines: "))
            temp_data_of_linesStringStorage = ''
            try:
                for j in range(1, count_of_lines+1):
                    for x in range(1, count_of_columns+1):
                        item = input(f"line:{j} item:{temp_data_of_columnsArray[x-1]} >")
                        # todo: сделать обработку неправильного ввода, например когда забыли ввести INT
                        item = item.split()
                        #print(item)
                        item_type = type_finder(item[0])
                        def if_item_is_null(item, temp_data_of_columnsArray):
                            if 'null' in item or 'Null' in item or 'NULL' in item:
                                print(f"item:{temp_data_of_columnsArray[x-1]} can't be null")
                                item = input(f"line:{j} item:{temp_data_of_columnsArray[x-1]} >")
                                if_item_is_null(item, temp_data_of_columnsArray[x-1])
                            return item
                        item = if_item_is_null(item, temp_data_of_columnsArray)
                        if item_type == 'int' or item_type == 'float':
                            temp_data_of_linesStringStorage += item[0] + ', '
                        else:
                            temp_data_of_linesStringStorage += '\''+item[0]+'\''+', '
                        
                    temp_data_of_lines.append(temp_data_of_linesStringStorage)
                    
                    temp_data_of_linesStringStorage = ''
                    #print(temp_data_of_lines, sep='\n')
            except Exception as e: 
                print(e)
                input("Back to main menu")
                main_menu()
            try:
                temp_data_of_columns_ready = ''
                temp_data_of_linesStringStorage2 = ''
                for i in range(len(temp_data_of_columnsArray)):
                    temp_data_of_columns_ready += temp_data_of_columnsArray[i] + ", "
                    
                for j in range(count_of_lines):
                    temp_data_of_linesStringStorage2 = temp_data_of_lines[j]
                    try:
                        cur.execute(f'''INSERT INTO {table_name} ({temp_data_of_columns_ready[:-2]})
                        VALUES ({temp_data_of_linesStringStorage2[:-2]})''')
                    except Exception as e: 
                        cur.execute("rollback")
                        print(e)
                        input('Something went wrong while inserting lines..')
                        main_menu()
                con.commit()
                print("Success!")
                try: 
                    cur.execute(f'''SELECT * FROM {table_name}''')
                except:
                    cur.execute("rollback")
                query_output_logic(cur.fetchall(), cur.description)
                input("Back to main menu")
                main_menu()
            except Exception as e: 
                print(e)
                input("Back to main menu")
                main_menu()

        def create_only(table_name):
            temp_data_of_columns = ''
            temp_data_of_columnsArray = []
            count_of_columns = int(input("Count of columns: "))
            print("Example: Id INT AUTO_INCREMENT")
            for i in range(1, count_of_columns+1):
                columns = input(f"column:{i} : ")
                temp_data_of_columnsArray.append(columns.split()[0])
                temp_data_of_columns += columns + ", "
                temp_data_of_columns = temp_data_of_columns.strip('\n')
            try:
                cur.execute(f'''CREATE TABLE {table_name} 
                ({temp_data_of_columns[:-2]})''')
                con.commit()
                print("Success!")
                #VALUES ({temp_data_of_lines[0]})''')
            except Exception as e:
                print("Error!", e)
                cur.execute("rollback")
            return temp_data_of_columns, temp_data_of_columnsArray, count_of_columns
        
        decision = input(f"Do you want to add some data in {table_name}? (Y/n) n - default :")
        if decision.lower() == 'y': create_and_fill(table_name)
        else: create_only(table_name)
        

class Deletor(Commands):
    def __init__(self, table_name):
        self.table_name = table_name
    
    def base_method(self, con, commands):
        #cur = super().base_method(commands, con)
        print(f"Confirm deleting the {self.table_name}. Enter the database name.")
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

#DataOfDatabases = DatabasesNames(input('Database name: ', input("Table name: ")))
def query_output_logic(rows, columns_from_cur):
    coulums = [] # array of columns names
    for i in range(len(columns_from_cur)): # filling colums by cur.description
        coulums.append((columns_from_cur[i][0]).upper())
            
    dt = [] # empty array of elements
    for row in rows: # filling array of elements
        for element in row:
            element = str(element).strip() # deleting ussles characters from the string
            dt.append(element)
    rtable = PrettyTable(coulums) # creating table
    while dt: # formatting table
        column = len(coulums)
        rtable.add_row(dt[:column])
        dt = dt[column:]
    clear()
    print(rtable)

def connec_db():
    try:
        # TODO: сделать подключение к бд и создать зашифрованный файл с информацией, при успешном коннекте
        #) TODO: сделать подключение к бд и заполение пользователем только пароля. все остальное хранится в атрибутах класса
        # TODO: сделать возможность подключения по строке подключения
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
        info = []
        empty_or_not = empty_or_not.st_size
        def read_from_non_empty_file():
            with open('info.txt', 'r') as f:
                for line in f:
                    info.append(line[:-1])
                return info
        def empty():
            with open('info.txt', 'w+') as f:
                f.write(input("Database name: ")+'\n')
                f.write(input("Host name: ")+'\n')
                f.write(input("Port: ")+'\n')
                f.write(input("User name: ")+'\n')
            return read_from_non_empty_file()
        if empty_or_not == 0:
            empty()
        else:
            decision = input("Restore previous session? (Y/n): Y - default : ")
            if "n" in decision.lower():
                info = empty()
            else:
                info = read_from_non_empty_file()
                
        #print(info)
        global con
        con = psycopg2.connect(
            database=info[-4],
            user=info[-1],
            password=stdiomask.getpass(),
            host=info[-3],
            port=info[-2]
            )
        print("Opened successfully")
        global cur
        cur = con.cursor()
        clear()
        return con
    except psycopg2.OperationalError:
        print (f'Could not connect to database server. Check your credentials')
        exit(0)


connec_db()
def main_menu():
    try:
        #clear()
        # TODO: подумать над Status()
        # TODO: Возможность просмотра таблиц
        DataOfDatabases = Status()
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

            cur.execute("""SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;""")
            print("Available tables:", *(str(*i) for i in cur.fetchall()))
            
        except:
            print("You don't have tables in your schema! \nLet's create a new table!")
            cur.execute("rollback")
        print("Write EOF in the end of query or pres ENTER twice")
        commands = input("SQL >> ")
        if commands == '1':
            clear()
            command = Creator(1)
            command.base_method(commands, con)
        elif commands == '2':
            clear()
            command = Deletor(input("Enter the name of the table: "))
            command.base_method(con, commands)
        elif commands == '3':
            clear()
            command = Selector(3)
            command.base_method(commands, con)
        elif commands == '4':
            exit(0)
        else:
            create_and_execute_ready_query(commands.strip("\n"))
            #print (f"Unknown option '{unknown_command}'")
            main_menu()
    except Exception as e: 
        print (f"Exception occurred while executing command. {e}")
        input('Back to main menu')
        main_menu()
    except KeyboardInterrupt:
        main_menu()
    finally:
        con.close()
        #clear()
        print("Closed successfully")
main_menu()
