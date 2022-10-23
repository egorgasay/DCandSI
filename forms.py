from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, HiddenField, TextAreaField, PasswordField, IntegerField


class CommonForm(FlaskForm):
    text = TextAreaField(label='Текст запроса',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 180px; width: 60%; ',
                         }
                         )
    submit = SubmitField("Выполнить",
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 80px; width: 10%; font-size: 14px'
                         }
                         )

class PostgresForm(FlaskForm):
    list_db = [('yes', 'Да'), ('No', 'Нет')]
    bdname = TextAreaField(label='Имя базы данных',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: 25%; ',
                         }
                         )
    hostname = TextAreaField(label='Имя хоста',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: 25%; ',
                         }
                         )
    port = IntegerField(label='Порт',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: 15%; ',
                         }
                         )
    username = TextAreaField(label='Имя пользователя',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: 25%; ',
                         }
                         )
    password = PasswordField(label='Пароль',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: 25%; ',
                         }
                         )
    remeber_db = SelectField(
        'Запомнить данные?',
        coerce=str,
        choices=list_db,
        render_kw={
            'class': 'form-control',
            'style': 'height: 30px; font-size: 14px'
        }
    )
    submit = SubmitField("Подключиться",
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 40px; width: 50%; font-size: 14px'
                         }
                         )

class ChooseForm(FlaskForm):
    list_db = [('PSQL', 'PostgreSQL'), ('MSSQL', 'Microsoft SQL Server')]
    db = SelectField(
        'Выберите СУБД',
        coerce=str,
        choices=list_db,
        render_kw={
            'class': 'form-control',
            'style': 'height: 30px; font-size: 14px'
        }
    )
    submit = SubmitField("Далее",
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 40px; width: 10%; font-size: 14px'
                         }
                         )

class LoginForm(FlaskForm):
    username = TextAreaField(label='Имя пользователя',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: 25%; ',
                         }
                         )
    password = PasswordField(label='Пароль',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: 25%; ',
                         }
                         )
    submit = SubmitField("Войти",
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 40px; width: 50%; font-size: 14px'
                         }
                         )

class RegForm(FlaskForm):
    username = TextAreaField(label='Имя пользователя',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: 25%; ',
                         }
                         )
    password = PasswordField(label='Пароль',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: 25%; ',
                         }
                         )
    password2 = PasswordField(label='Пароль',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: 25%; ',
                         }
                         )
    submit = SubmitField("Зарегистрироваться",
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 40px; width: 50%; font-size: 14px'
                         }
                         )