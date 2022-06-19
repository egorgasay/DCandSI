import psycopg2
from prettytable import PrettyTable
import random as rnd
import os

class DatabasesNames:
    def __init__(self, database, table_name):
        self.database = database
        # TODO: сделать атрибутом по умлочанию
        self.table_name = table_name

class Commands:
    table = 'table'
    def __init__(self, command):
        self.command = command
    def base_method(self, commands, con):
        cur = con.cursor()
        return cur

class Selector(Commands):
    def base_method(self, commands, con, table_name):
        ''' updates base_method from the Command module
        '''
        cur = super().base_method(commands, con)
        #!@lru_cache
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
            print(rtable)
        def decision_func(cur, table_name):
            '''Forces you to make a choice between two options
            '''
            print("Do you need a complex(1) or simple(2) query?")
            decision = input("# ")
            if decision == str(2):
                '''simple query
                '''
                print(f"What colums do you need to select from {table_name}?")
                # getting user input (names of columns or ALL columns)
                user_columns = input("Example: age, gender, username or ALL: ")
                # check the input for the presence of ALL
                if user_columns.lower() == "all": user_columns = "*"
                # execute cursor
                cur.execute(f'''SELECT {user_columns} FROM {table_name}''')
                #rows = cur.fetchall() # getting the data from the database
                query_output_logic(cur.fetchall(), cur.description)
                
            elif decision == str(1):
                '''complex query
                '''
                print("This module in development mode")
                def decision2_func():
                    print("Do you want to type query manualy(1) or execute ready query from a file(2) ?")
                    decision2 = input("# ")
                    if decision2 == str(1):
                        print("Write EOF in the end of query or pres ENTER twice")
                        print("SQL ")
                        query, enter = '', 1
                        user_query = input(">>>: ").strip("\n")
                        text_of_query = [user_query]
                        while user_query != 'EOF' and enter != 2:
                            query += user_query + " "
                            user_query = input(">>>: ").strip("\n")
                            text_of_query.append(user_query)
                            if user_query == '':
                                user_query = i if (i:=input(">>>: ").strip("\n")) != 'EOF' else ''
                                text_of_query.append(user_query)
                                if user_query == '':
                                    enter = 2
                        
                        cur.execute(f'''{query}''')
                        query_output_logic(cur.fetchall(), cur.description)
                        save_decision = input("Save the query text? (Y/n): ")
                        text_of_query = list(filter(None, text_of_query))
                        if save_decision.lower() == 'n' or save_decision.lower() == 'no':
                            pass
                        else:
                            file_name = 'query_'+str(rnd.randint(0, 100000))+'.txt'
                            with open(file_name, 'w+') as f:
                                for line in range(len(text_of_query)):
                                    f.write(text_of_query[line]+'\n')
                            print(f"Saved in {file_name}")
                    elif decision2 == str(2):
                        def file_executor(file_name=''):
                            if file_name == '':
                                file_name = input("File name or path to the file: ")
                            if file_name.count("/") != 0:
                                file_name.replace("/", "\\\\")
                                print(file_name)
                            with open(file_name, 'r') as f:
                                    text_of_query = []
                                    for line in f:
                                        text_of_query.append(line.strip('\n'))
                            query =  ' '.join(text_of_query)
                            cur.execute(f'''{query}''')
                            query_output_logic(cur.fetchall(), cur.description)
                            decision = input("Do you want to run the query again? (Y/n) y - Default: ")
                            if decision.lower() == 'n' or decision.lower() == 'no':
                                main_menu()
                            file_executor(file_name)
                        file_executor()
                        
                        
                    else:
                        # TODO: сделать try except error рекурсии
                        print("Please select 1 or 2")
                        decision2_func()
                decision2_func()

            else:
                # TODO: сделать try except error рекурсии
                print("Please select 1 or 2")
                decision_func(cur)
        decision_func(cur, table_name)
        


# class Insertor(Command):
#     def base_method(self):
#         cur.execute(f'''INSERT INTO {DataOfDatabases.table} '''


#DataOfDatabases = DatabasesNames(input('Database name: ', input("Table name: ")))

def main_menu():
    DataOfDatabases = DatabasesNames('test_for_python', 'student')
    try:
        con = psycopg2.connect(
            database=DataOfDatabases.database,
            user='test_user',
            password='xxXX1234',
            host='localhost',
            port='5433'
            )
        print("Opened successfully")
        print("Options:")
        x = ['Create a new table', 'Delete a table', 'Create a new query']
        for i in range(len(x)): print(str(i+1) + ' ' + x[i])
        match (commands:= int(input())):
            case 1:
                command = Commands(1)
            case 2:
                command = Commands(2)
            case 3:
                command = Selector(3)
                command.base_method(commands, con, DataOfDatabases.table_name)
            # case 4:
            #     command = Commands(4)
            case unknown_command:
                print (f"Unknown option '{unknown_command}'")
    except psycopg2.OperationalError:
        print (f'Could not connect to database server')
        exit(0)
    finally:
        print("Closed successfully")
main_menu()