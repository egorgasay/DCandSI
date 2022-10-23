import os
import platform
import sqlite3
from clear_screen import clear
from psycopg2 import Error
from query import Query
from create import Creator
from delete import Deletor
from connect import ConnectDB
from functions import create_and_execute_ready_query, query_output_logic, tables_list
from colorama import init, Fore
from colorama import Back
from colorama import Style
from forms import CommonForm, ChooseForm, PostgresForm, RegForm, LoginForm
import random
from flask import Flask, render_template, session, redirect, url_for, request, g, make_response


def app_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    randArray = []
    for i in chars:
        randArray.append(chars[random.randint(0, len(chars) - 1)])
    return ''.join(randArray)


app = Flask(__name__)
app.config['SECRET_KEY'] = app_secret_key()
# app.config['DATABASE'] = os.getcwd()+'dcsi.sqlite'
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'dcsi.sqlite')))
# session.permanent = True


def connect_db_for_auth():
    global conn
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def connection():
    #global connect
    #connect = ConnectDB()
    global conn
    conn = connect_db_for_auth()
    data = connect_instance.connec_db(conn)
    print('''
    _                                _
    | \  _. _|_  _. |_   _.  _  _    /   _  ._  _|_ ._  _  | |  _  ._
    |_/ (_|  |_ (_| |_) (_| _> (/_   \_ (_) | |  |_ |  (_) | | (/_ |
        __         ___
    ()    (_   _. |    |  ._  _|_  _  ._ ._  ._  _  _|_  _  ._
    (_X   __) (_| |   _|_ | |  |_ (/_ |  |_) |  (/_  |_ (/_ |
                |                        |
    ''')
    print("новое подключение")
    return data


@app.route('/reg', methods=['POST', 'GET'])
def reg():
    form = RegForm()
    if form.validate_on_submit():
        uname = form.username.data
        pswd = form.password.data
        pswd2 = form.password2.data
        conn = connect_db_for_auth()
        if pswd == pswd2:
            connect = ConnectDB()
            scode = connect.create_user(uname, pswd, conn)
            if scode == 'OK':
                return redirect(url_for('login'))
            elif scode == 'The username is already taken':
                return '<h1>The username is already taken</h1>'
            return '<h1>Error</h1>'
        return '<h1>Error</h1>'
    return render_template('reg.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    # log = ""
    if not session.get('logged'):
        session.setdefault('logged', 'no')
    # print([log])
    if session['logged'] == 'yes':
        return redirect(url_for('web_app'))
    form = LoginForm()
    if form.validate_on_submit():
        uname = form.username.data
        pswd = form.password.data
        conn = connect_db_for_auth()
        try:
            cur = conn.cursor()
            global connect_instance
            connect_instance = ConnectDB()
            connect_instance.main_username = uname
            access = connect_instance.compare_passwords(uname, pswd, cur)
            # data = cur.execute(f'''SELECT password FROM Users WHERE username = "{uname}"''')
            # passwd_from_db = tuple(data.fetchone())
        except Exception as e:
            print(str(e))
            return '<h1>Error</h1>'
        # access = True if passwd_from_db[0] == pswd else False
        print(access)
        if access == 'OK':
            session['logged'] = 'yes'
            # res = make_response(f"<h1>Форма авторизации</h1>logged: {log}")
            # res.set_cookie("logged", "yes")
            # print(request.cookies.get('logged'))

            # return redirect(url_for('route_logic'))
            # return res
        # if request.cookies.get('logged')
        #conn.close() МБ ТУТ НАДО ПОПРАВИТЬ
        #global data
        #data = connection()
        return redirect(url_for('web_app')) if access else '<h1>Wrong password</h1>'
    return render_template('login.html', form=form)

# @app.route('/route_logic', methods=['POST', 'GET'])
# def route_logic():
#     log = request.cookies.get('logged')
#     if request.cookies.get('logged') != 'yes':
#         res = make_response(f"<h1>Форма авторизации</h1>logged: {log}")
#         res.set_cookie("logged", "yes")
#         return redirect(url_for('web_app'))
#     return redirect(url_for('login'))


@app.route('/main', methods=['POST', 'GET'])
def web_app():
    data = connection()
    log = ''
    # print(1)
    if not session.get('logged'):
        return redirect(url_for('login'))
    print(2)
    if session['logged'] != 'yes':
        return redirect(url_for('login'))
    form = CommonForm()
    text = form.text.data
    available_tables = ''
    print(3)
    if not text and request.method == 'GET' or text == '':
        try:
            #global data
            if data:
                pass
        except:
            data = connection()
    # data = connect.read_from_non_empty_file()
    # print(logo)
    try:
        if data:
            pass
    except TypeError:
        data = connection()
    except NameError:
        data = connection()
    print(data)
    if 'Wrong credentials' in data:
        conn = connect_db_for_auth()
        connect_instance = ConnectDB()
        conn.cursor().execute(
            f"""DELETE FROM Data WHERE db_name = (SELECT db_name FROM Data WHERE username = '{connect_instance.main_username}')  """)
        conn.commit()
        print('succ')
        return redirect(url_for('start_page'))
    if 'No data in table' in data:
        return redirect(url_for('start_page'))
    if 'Nothing' in data:
        return redirect(url_for('start_page'))
    global con, info, cur
    con, info, cur = [*data]

    available_tables = tables_list(cur, info[-1])
    if text:
        command = Query()
        try:
            cur.execute(text)
            # global data_from_query
            data_from_query = cur.fetchall()
            descr_column = cur.description
            table = query_output_logic(
                data_from_query, cur.description).get_html_string()
        except Exception as e:
            e = str(e)
            if 'no results to fetch' in e:
                table = '<h1>Нет данных для отображения</h1>'
            elif 'already exists' in e and 'relation' in e:
                table = '<h1>Таблица уже существует</h1>'
            else:
                table = f'<h1>{e}</h1>'
                try:
                    cur.execute("rollback")
                except:
                    table += '<br><h2>Еще ошибка при rollback</h2>'
            print(e)
            available_tables = tables_list(cur, info[0])
        con.commit()
        return render_template('index.html', available_tables=available_tables, form=form, table=table)
    return render_template('index.html', available_tables=available_tables, form=form)

# @app.route('/api/data')
# def data():
#     return {'data': [row.to_dict() for row in data_from_query]}


@app.errorhandler(404)
def pageNotFound(error):
    return redirect(url_for('web_app'))


@app.route('/postgres', methods=['post', 'get'])
def postgres():
    if not session.get('logged'):
        session.setdefault('logged', 'no')
    if session['logged'] != 'yes':
        return redirect(url_for('login'))
    form = PostgresForm()
    if form.validate_on_submit():
        # print(form.username.data)
        # with open('info.txt', 'w+') as f:
        #     f.write('1' + '\n')
        #     f.write(form.username.data + '\n')
        #     f.write(form.password.data + '\n')
        #     f.write(form.bdname.data + '\n')
        #     f.write(form.hostname.data + '\n')
        #     f.write(form.port.data + '\n')
        #     f.write(form.remeber_db.data + '\n')
        conn = connect_db_for_auth()
        connect.record_user_db(conn, form.hostname.data, form.bdname.data,
                               form.username.data, form.password.data, form.port.data, 'PSQL')
        # connect = ConnectDB
        # data = connect.connec_db()
        return redirect(url_for('web_app'))
    else:
        print(form.errors)
    return render_template('example.html', form=form)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    # request.cookies.set('logged', 'no')
    session['logged'] = 'no'
    # res = make_response("Вы больше не авторизованы!</p>")
    # res.set_cookie("logged", "", 0)
    # if request.cookies.get('logged') == 'yes':
    #     return res
    return redirect(url_for('login'))
    # os.remove('info.txt')
    # return redirect(url_for('start_page'))


@app.route('/', methods=['post', 'get'])
def start_page():
    # try:
    #     conn = ConnectDB()
    #     cur = conn.cursor()

    #     # if os.stat('info.txt').st_size > 0:
    #     #     return redirect(url_for('web_app'))
    # except Exception as e:
    #     print(e)
    if not session.get('logged'):
        session.setdefault('logged', 'no')
    if session['logged'] != 'yes':
        return redirect(url_for('login'))
    username = connect_instance.main_username
    print([username])
    # print(username)
    conn = connect_db_for_auth()
    print(conn)
    try:
        data_from_query = conn.cursor().execute(
            f"""SELECT username FROM Data WHERE username = '{username}'""")
        data_from_query = tuple(data_from_query.fetchone())[0]
        #print('uname', data_from_query)
    except sqlite3.ProgrammingError:
        print('sqlite3.ProgrammingError')
        # conn.close()
        # conn = connection()
        # data_from_query = conn.cursor().execute(
        # f"""SELECT username FROM Data WHERE username = '{username}'""")
        # return redirect(url_for('web_app'))
    try:
        if data_from_query == username:
            #print('redirect')
            return redirect(url_for('web_app'))
    except:
        print()
    form = ChooseForm()
    if form.validate_on_submit():
        if form.db.data == 'PSQL':
            return redirect(url_for('postgres'))
        elif form.db.data == 'MSSQL':
            return 'Developing'
    return render_template('example.html', form=form)

# @app.teardown_appcontext
# def close_db(error):
#     if hasattr(g, 'link_db'):
#         g.link_db.close()


def main_menu(*args):
    try:
        # clear()
        # TODO: Id INT AUTO_INCREMENT
        # if args:
        #    global con, info, cur
        #    con, info, cur = [*args[0]]

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
    # decision = ''
    # while decision != '1' and decision != '2':
    #     print("1. Web Server mode\n2. Terminal mode")
    #     decision = input("Выберите 1 или 2: ")
    # if decision == '2':
    #     main_menu()
    # else:
    app.run(host='0.0.0.0', debug=True)
    session.permanent = True
    start_page()
