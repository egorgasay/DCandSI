import os
import platform
from sqlite3 import connect
from clear_screen import clear
from psycopg2 import Error
from query import Query
from create import Creator
from delete import Deletor
from connect import ConnectDB
from functions import create_and_execute_ready_query, query_output_logic
from colorama import init, Fore
from colorama import Back
from colorama import Style
from flask import Flask, render_template
from forms import CommonForm
import random

def app_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    randArray = []
    for i in chars:
        randArray.append(chars[random.randint(0,len(chars)-1)])
    return ''.join(randArray)

app = Flask(__name__)
app.config['SECRET_KEY'] = app_secret_key()

@app.route('/', methods=['POST', 'GET'])
def web_app():
    form = CommonForm()
    text = form.text.data
    available_tables = ''
    if not text:
        global connect
        connect = ConnectDB()
        global data
        data = connect.connec_db()
    
    if data:
        global con, info, cur
        con, info, cur = [*data]
    
    if info[0] == '3':
        # for row in list_tables: row.table_name
        tables_names = [*(str(i.table_name) for i in cur.tables())]
        available_tables = f"{', '.join(tables_names)}."
    else:
        try:
            if info[0] == '1':
                cur.execute( """SELECT table_name FROM information_schema.tables WHERE table_schema='public' ORDER BY table_name;""")
                tables_names = [*(str(*i) for i in cur.fetchall())]
                available_tables = f"{', '.join(tables_names)}."
            elif info[0] == '2':
                cur.execute("""SELECT name FROM sys.tables""")
                tables_names = [*(str(*i) for i in cur.fetchall())]
                available_tables = f"{', '.join(tables_names)}."

        except Exception as e:
            print(e)
            available_tables = "You don't have tables in your schema! \nLet's create a new table!"
            try:
                cur.execute("rollback")
            except:
                print('')
    if text:
        command = Query()
        #command.base_method(con)
        #print([text])
        #print(data())
        cur.execute(text)
        global data_from_query
        data_from_query = cur.fetchall()
        descr_column = cur.description
        table = query_output_logic(data_from_query, cur.description).get_html_string()
        #print(len(table.get_html_string()))
        #print(table.get_html_string())
        #for line in answer:
        #    ready.append([word for word in line[:-1].split(' ')])

        return render_template('index.html', available_tables=available_tables, form=form, table=table)
    return render_template('index.html', available_tables=available_tables, form=form)

@app.route('/api/data')
def data():
    return {'data': [row.to_dict() for row in data_from_query]}

def main_menu(*args):
    try:
        # clear()
        # TODO: Id INT AUTO_INCREMENT
        #if args:
        #    global con, info, cur
        #    con, info, cur = [*args[0]]
        
        print('''
         _                                _
        | \  _. _|_  _. |_   _.  _  _    /   _  ._  _|_ ._  _  | |  _  ._  
        |_/ (_|  |_ (_| |_) (_| _> (/_   \_ (_) | |  |_ |  (_) | | (/_ |   
               __         ___                                              
        ()    (_   _. |    |  ._  _|_  _  ._ ._  ._  _  _|_  _  ._       
        (_X   __) (_| |   _|_ | |  |_ (/_ |  |_) |  (/_  |_ (/_ |
                    |                        |                             
        ''')
        global available_tables
        available_tables = 'No tables!'
        
        web_app(con, info, cur)
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
    except (Exception, Error) as error:
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
    app.run()
    web_app()
