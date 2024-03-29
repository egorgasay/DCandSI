from prettytable import PrettyTable
from clear_screen import clear
import random as rnd
from colorama import init, Fore
from colorama import Back
from colorama import Style
import os

def get_col_name(col_act_name):
    if not col_act_name[-1].isdigit():
        col_act_name += '-1'
    elif col_act_name[-1].isdigit():
        col_act_name += str(int(col_act_name[-1]) + 1)
    return col_act_name

def query_output_logic(rows, columns_from_cur):
    """ 
    Query output logic
    """
    coulums = []  # array of columns names
    for i in range(len(columns_from_cur)):  # filling colums by cur.description
        col_act_name = (columns_from_cur[i][0]).upper()
        if col_act_name in coulums:
            col_act_name = get_col_name(col_act_name)
        coulums.append((col_act_name))
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
    #clear()
    return rtable


def file_executor(cur, file_name=''):
    """ 
    Executing a query from a file
    """
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
        input(
            Fore.RED + f"Exception occurred while collecting text of query. {e}" + Style.RESET_ALL)
        file_executor(cur)
    query = ' '.join(text_of_query)
    try:
        cur.execute(f'''{query}''')
        query_output_logic(cur.fetchall(), cur.description)
    except Exception as e:
        cur.execute("rollback")  # rollback if query is bad
        input(Fore.RED + f"Something went wrong while executing query.. \n{e}" +
              Style.RESET_ALL)

    decision = input("Do you want to run the query again? (Y/n) y - Default: ")
    if decision.lower() == 'n' or decision.lower() == 'no':
        return 0
    file_executor(cur, file_name)


def create_and_execute_ready_query(user_query, con):
    """ 
    Creating and executing ready query
    """
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
        file_executor(cur, file_name)
        con.commit()
        return 0
    # print("Closed successfully")
    # exit(0)
    #
    try:
        print(query)
        cur.execute(query)
    except Exception as e:
        cur.execute("rollback")
        input(Fore.RED + f"{e}" + Style.RESET_ALL)
        input("Back to main menu")
        clear()
        return 0

    try:
        query_output_logic(cur.fetchall(), cur.description)
    except Exception as e:
        if 'o results' in str(e):
            print("No results to fetch! Check your query if you were expecting output.")
        else:
            input(Fore.RED + f"{e}!" + Style.RESET_ALL)
            input("Back to main menu")
            return 0
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
        clear()
    con.commit()

def tables_list(cur, baseid):
    available_tables = ''
    if baseid == '3':
        # for row in list_tables: row.table_name
        tables_names = [*(str(i.table_name) for i in cur.tables())]
        available_tables = f"{', '.join(tables_names)}."
    else:
        try:
            if baseid == 'PSQL':
                cur.execute( """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;""")
                data_from_query = cur.fetchall()
                if len(data_from_query) == 1:
                    available_tables = [data_from_query[0][0]]
                else:
                    tables_names = [*(str(*i) for i in data_from_query)]
                    available_tables = tables_names #f"{', '.join(tables_names)}."
            elif baseid == '2':
                cur.execute("""SELECT name FROM sys.tables""")
                data_from_query = cur.fetchall()
                tables_names = [*(str(*i) for i in data_from_query)]
                available_tables = f"{', '.join(tables_names)}."

        except Exception as e:
            print(e)
            available_tables = "You don't have tables in your schema! \nLet's create a new table!"
            try:
                cur.execute("rollback")
            except:
                print('')
        return available_tables