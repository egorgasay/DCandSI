import os
import platform
import sqlite3
from time import sleep
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
from forms import *
#CommonForm, ChooseForm, PostgresForm, RegForm, LoginForm
import random
from flask import Flask, render_template, session, redirect, url_for, request, g, make_response, flash


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
    #global conn
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
    if session.get('logged') == 'yes':
        return redirect(url_for('web_app'))
    form = RegForm()
    if form.validate_on_submit():
        uname = form.username.data
        pswd = form.password.data
        pswd2 = form.password2.data
        conn = connect_db_for_auth()
        text_for_user = ''
        if pswd == pswd2:
            connect = ConnectDB(conn, 'TempUserName')
            scode = connect.create_user(uname, pswd, conn)
            if scode == 'OK':
                flash('Регистрация прошла успешно!',  category='success')
                return redirect(url_for('login'))
            elif scode == 'The username is already taken':
                text_for_user = 'Имя пользователя занято'
            else:
                text_for_user = 'Ошибка'
        else:
            text_for_user = 'Пароли не совпадают'
        flash(text_for_user,  category='error')
    return render_template('reg.html', form=form)


@app.route('/login', methods=['POST', 'GET'])
def login():
    # log = ""
    if not session.get('logged'):
        session.setdefault('logged', 'no')
    if not session.get('id'):
        session.setdefault('id', random.randint(1, 100000000))
    # print([log])
    if session.get('logged') == 'yes':
        return redirect(url_for('web_app'))
    form = LoginForm()
    if form.validate_on_submit():
        uname = form.username.data
        pswd = form.password.data
        conn = connect_db_for_auth()
        try:
            cur = conn.cursor()
            try:
                global connect_instance
                if connect_instance:
                    pass
            except Exception as e:
                print(str(e), 'error instance not exists and its fine')
                connect_instance = dict()
            connect_instance[str(session.get('id'))] = ConnectDB(conn, uname)
            connect_instance[str(session.get('id'))] = [connect_instance[str(session.get('id'))], connect_instance[str(session.get('id'))].main_username, conn]
            access = connect_instance[str(session.get('id'))][0].compare_passwords(uname, pswd, cur)
        except Exception as e:
            print(str(e))
            flash(f'{e}',  category='error')
        print('aaa', access)
        if access == 'OK':
            session['logged'] = 'yes'
            return redirect(url_for('web_app'))
        else:
            flash('Неверное имя пользователя',  category='error')  if access == 'Wrong username' else flash('Неверный пароль',  category='error')
    return render_template('login.html', form=form)


@app.route('/main', methods=['POST', 'GET'])
def web_app():
    print(session.get('user_id'))
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
            data = connect_instance[str(session.get('id'))][0].connec_db(connect_db_for_auth())
    try:
        if data:
            pass
    except TypeError:
        data = connect_instance[str(session.get('id'))][0].connec_db(connect_db_for_auth())
    except NameError:
        data = connect_instance[str(session.get('id'))][0].connec_db(connect_db_for_auth())
    #print(data)
    if 'Wrong credentials' in data:
        if connect_instance[str(session.get('id'))][0]:
            flash('Неверные данные', category='error')
            return redirect(url_for('disconnect'))
        return redirect(url_for('start_page'))
    if 'No data in table' in data:
        return redirect(url_for('start_page'))
    if 'Nothing' in data:
        return redirect(url_for('start_page'))
    global con, info, cur
    con, info, cur = [*data]
    #print(data)
    available_tables = tables_list(cur, info[-1])
    ListOfTablesForm = ''
    # if available_tables:
    #     double_tables = [(i, i) for i in available_tables_list]
    #     print(double_tables)

    if text:
        command = Query()
        available_tables = tables_list(cur, info[0])
        data_from_query = ""
        try:
            cur.execute(f'SELECT * FROM ({text}) AS OUT LIMIT 1000')
            data_from_query = cur.fetchall()
            # global data_from_query
            #table = query_output_logic(data_from_query, cur.description).get_html_string()
        except Exception as e:
            table = ''
            e = str(e)
            if 'no results to fetch' in e:
                flash('Нет данных для отображения')
            elif 'already exists' in e and 'relation' in e:
                flash('Таблица уже существует')
            else:
                flash(f'{e}',  category='error')
                try:
                    cur.execute("rollback")
                except:
                    flash('Ошибка при rollback', category='error')
            print(e)
        descr_column = cur.description
        con.commit()
        available_tables = tables_list(cur, info[-1])
        data_for_table = [list(i) for i in data_from_query]
        return render_template('index.html', available_tables=available_tables, form=form, description=descr_column, data=data_for_table)
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
        conn = connect_db_for_auth()
        # session['main_username']
        connect = connect_instance[str(session.get('id'))][0]
        connect.record_user_db(conn, form.hostname.data, form.bdname.data,
                               form.username.data, form.password.data, form.port.data, 'PSQL')
        # connect = ConnectDB
        # data = connect.connec_db()
        return redirect(url_for('web_app'))
    else:
        print(form.errors)
    return render_template('example.html', form=form)

@app.route('/main/<string:table_name>', methods=['POST', 'GET'])
def get_all_data_from_table(table_name):
    if not session.get('logged'):
        session.setdefault('logged', 'no')
    if session['logged'] != 'yes':
        return redirect(url_for('login'))
    cur = connect_instance[str(session.get('id'))][0].connec_db(connect_db_for_auth())[2]
    cur.execute(f'''SELECT * FROM "{table_name}" LIMIT 1000''')
    data_from_query = cur.fetchall()
    data = [list(i) for i in data_from_query]
    #print(data)
    return render_template('get_all_data_from_table.html', table_name=table_name, description=cur.description, data=data)

@app.route('/logout', methods=['POST', 'GET'])
def logout():
    session['logged'] = 'no'
    return redirect(url_for('login'))

@app.route('/create_table', methods=['POST', 'GET'])
def create_table():
    return '<style>body {background:black}</style><div style="align-items: center; justify-content: center;display:flex;align-items: center;height:100%"><h1 style="text-align:center; color:white">В разработке</h1>'
    #return render_template('create_table.html')

@app.route('/delete_table', methods=['POST', 'GET'])
def delete_table():
    return '<style>body {background:black}</style><div style="align-items: center; justify-content: center;display:flex;align-items: center;height:100%"><h1 style="text-align:center; color:white">В разработке</h1>'
    #return render_template('create_table.html')

@app.route('/req_from_file', methods=['POST', 'GET'])
def req_from_file():
    return '<style>body {background:black}</style><div style="align-items: center; justify-content: center;display:flex;align-items: center;height:100%"><h1 style="text-align:center; color:white">В разработке</h1>'
    #return render_template('create_table.html')

@app.route('/simple_request', methods=['POST', 'GET'])
def simple_request():
    return '<style>body {background:black}</style><div style="align-items: center; justify-content: center;display:flex;align-items: center;height:100%"><h1 style="text-align:center; color:white">В разработке</h1>'
    #return render_template('create_table.html')


@app.route('/disconnect', methods=['POST', 'GET'])
def disconnect():
    main_username, conn = connect_instance[str(session.get('id'))][1], connect_db_for_auth()
    conn.cursor().execute(
        f"""DELETE FROM Data WHERE db_name = (SELECT db_name FROM Data WHERE username = '{main_username}')  """)
    conn.commit()
    print('успешно удалено')
    return redirect(url_for('start_page'))

@app.route('/', methods=['post', 'get'])
def start_page():
    if not session.get('logged'):
        session.setdefault('logged', 'no')
    if session['logged'] != 'yes':
        return redirect(url_for('login'))
    username = connect_instance[str(session.get('id'))][1]
    print([username])
    # print(username)
    conn = connect_instance[str(session.get('id'))][2]
    print(conn)
    try:
        data_from_query = conn.cursor().execute(
            f"""SELECT username FROM Data WHERE username = '{username}'""")
        data_from_query = tuple(data_from_query.fetchone())[0]
        #print('uname', data_from_query)
    except sqlite3.ProgrammingError:
        print('sqlite3.ProgrammingError')
    except TypeError:
        pass
    try:
        if data_from_query == username:
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)
    session.permanent = True
    start_page()
