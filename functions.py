from prettytable import PrettyTable
from clear_screen import clear
import random as rnd


def query_output_logic(rows, columns_from_cur):
    """ 
    Query output logic
    """
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
        print(f"Exception occurred while collecting text of query. {e}")
        file_executor(cur)
    query = ' '.join(text_of_query)
    try:
        cur.execute(f'''{query}''')
        query_output_logic(cur.fetchall(), cur.description)
    except Exception as e:
        cur.execute("rollback")  # rollback if query is bad
        print(f"Something went wrong while executing query. {e}")
    decision = input("Do you want to run the query again? (Y/n) y - Default: ")
    if decision.lower() == 'n' or decision.lower() == 'no':
        return 0
        exit(0)
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
        file_executor(file_name)
        con.commit()
        return 0
        # print("Closed successfully")
        exit(0)
    #
    try:
        cur.execute(f'''{query}''')
    except Exception as e:
        cur.execute("rollback")
        print(e)
        input("Back to main menu")
        clear()
        return 0
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
        clear()
