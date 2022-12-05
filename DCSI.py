import datetime
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
        print('Статус авторизации:', access)
        if access == 'OK':
            session['logged'] = 'yes'
            return redirect(url_for('web_app'))
        else:
            flash('Неверное имя пользователя',  category='error')  if access == 'Wrong username' else flash('Неверный пароль',  category='error')
    return render_template('login.html', form=form)


@app.route('/main', methods=['POST', 'GET'])
def web_app():
    if not session.get('logged'):
        return redirect(url_for('login'))
    if session['logged'] != 'yes':
        return redirect(url_for('login'))
    form = CommonForm()
    try:
        text = request.form['text']
        #print(text)
    except:
        text = ""
    print("Проверка наличия существующего подключения")
    data = conn_check()
    try:
        if 'sqlite3' in str(data[0]).lower() or 'Wrong credentials' in data:
            flash('Неверные данные', category='error')
            return redirect(url_for('disconnect'))
        conn_id = str(data[0]).split(" ")[3]
    except IndexError:
        return redirect(url_for('disconnect'))

    print("Id подключения -", conn_id)
    if 'No data in table' in data:
        return redirect(url_for('start_page'))
    if 'Nothing' in data:
        return redirect(url_for('start_page'))
    global con, info, cur
    con, info, cur = [*data]
    available_tables = tables_list(cur, info[-1])
    if text:
        print("Поступил запрос:")
        print(text)
        data_from_query = ""
        try:
            username = connect_instance[str(session.get('id'))][0].main_username
            record_query(username, text)
            cur.execute(text)
            data_from_query = cur.fetchall()[:1000]
            con.commit()
        except Exception as e:
            e = str(e)
            if 'no results to fetch' in e:
                flash('Нет данных для отображения')
            elif 'already exists' in e and 'relation' in e:
                flash('Таблица уже существует')
            else:
                for eline in e.split('\n'):
                    flash(f'{eline}',  category='large_error')
                try:
                    cur.execute("rollback")
                except:
                    flash('Ошибка при rollback', category='error')
            print(e)
        descr_column = cur.description
        available_tables = tables_list(cur, info[-1])
        data_for_table = [list(i) for i in data_from_query]
        return render_template('index.html', available_tables=available_tables, form=form, description=descr_column, data=data_for_table)
    return render_template('index.html', available_tables=available_tables, form=form)

# @app.route('/api/data')
# def data():
#     return {'data': [row.to_dict() for row in data_from_query]}

def record_query(username, query):
    conn = connect_db_for_auth()
    try:
        time_now = datetime.datetime.now()
        conn.cursor().execute(
            f"""INSERT INTO querys (username, query, date) VALUES ("{username}","{query}", '{time_now}')""")
        conn.commit()
        print('Текст запроса успешно сохранен в базу данных')
    except sqlite3.ProgrammingError:
        print('sqlite3.ProgrammingError')
    except TypeError:
        pass

def conn_check():
    '''Проверка наличия существующего подключения'''
    if not connect_instance[str(session.get('id'))][0].info:
        data = connect_instance[str(session.get('id'))][0].connec_db(connect_db_for_auth())
    else:
         data_obj = connect_instance[str(session.get('id'))][0]
         data = [data_obj.con, data_obj.info, data_obj.cur]
    return data

@app.errorhandler(404)
def pageNotFound(error):
    return redirect(url_for('web_app'))

@app.route('/querys', methods=['post', 'get'])
def querys():
    if not session.get('logged'):
        session.setdefault('logged', 'no')
    if session['logged'] != 'yes':
        return redirect(url_for('login'))
    conn = connect_db_for_auth()
    main_user = conn_check()[1]
    querys_list = ""
    try:
        cur = conn.cursor()
        cur.execute(f'''SELECT query, date FROM querys WHERE username = "{main_user[0]}";''')
        querys_list = cur.fetchall()
    except Exception as e:
        print(e)
    return render_template('querys.html', querys_list=querys_list, len=len)

# def check_is_logged_in():
#     if not session.get('logged'):
#         session.setdefault('logged', 'no')
#     if session['logged'] != 'yes':
#         return redirect(url_for('login'))

@app.route('/list_of_tables', methods=['post', 'get'])
def list_of_tables():
    if not session.get('logged'):
        session.setdefault('logged', 'no')
    if session['logged'] != 'yes':
        return redirect(url_for('login'))
    if not session.get('logged'):
        session.setdefault('logged', 'no')
    if session['logged'] != 'yes':
        return redirect(url_for('login'))
    data = conn_check()
    cur, baseid = data[2], data[1][-1]
    available_tables = tables_list(cur, baseid)
    return render_template('list_of_tables.html', available_tables=available_tables)

@app.route('/postgres', methods=['post', 'get'])
def postgres():
    if not session.get('logged'):
        session.setdefault('logged', 'no')
    if session['logged'] != 'yes':
        return redirect(url_for('login'))
    form = PostgresForm()
    if form.validate_on_submit():
        conn = connect_db_for_auth()
        connect = connect_instance[str(session.get('id'))][0]
        connect.record_user_db(conn, form.hostname.data, form.bdname.data,
                               form.username.data, form.password.data, form.port.data, 'PSQL')
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
    cur = conn_check()[2]
    cur.execute(f'''SELECT * FROM public."{table_name}" LIMIT 1000''')
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
    if not session.get('logged'):
        session.setdefault('logged', 'no')
    if session['logged'] != 'yes':
        return redirect(url_for('login'))
    data = conn_check()
    cur, baseid = data[2], data[1][-1]
    available_tables = tables_list(cur, baseid)
    return render_template('delete_table.html', available_tables=available_tables)

@app.route('/delete_table/<string:table_name>', methods=['POST', 'GET'])
def deleting_table(table_name):
    data = conn_check()
    cur, conn = data[2], data[0]
    try:
        cur.execute(f'''DROP TABLE "{table_name}" ''')
        conn.commit()
    except:
        flash('Ошибка при удалению таблицы', category='error')
    else:
        flash('Таблица успешно удалена', category='success')
    return redirect(url_for('web_app'))

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
    main_username, conn = connect_instance[str(session.get('id'))][0].main_username, connect_db_for_auth()
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
