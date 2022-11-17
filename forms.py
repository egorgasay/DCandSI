from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, HiddenField, TextAreaField, PasswordField, IntegerField, StringField


class CommonForm(FlaskForm):
    text = TextAreaField(label='Текст запроса',
                         render_kw={
                             'style': 'height: 160px; width: 80%; font-size: 26px; background:#000000; color:#FFFFFF;',
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
    bdname = StringField(label='Имя базы данных',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: auto; ',
                         }
                         )
    hostname = StringField(label='Имя хоста',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: auto; ',
                         }
                         )
    port = IntegerField(label='Порт',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: auto; ',
                         }
                         )
    username = StringField(label='Имя пользователя',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: auto; ',
                         }
                         )
    password = PasswordField(label='Пароль',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: 30px; width: auto; ',
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
                             'style': 'height: auto; width: auto; font-size: 14px'
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
            'style': 'height: auto; font-size: 14px'
        }
    )
    submit = SubmitField("Далее",
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: auto; width: auto;font-size: 14px'
                         }
                         )

class LoginForm(FlaskForm):
    username = StringField(label='Никнейм',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: auto; width: auto; ',
                         }
                         )
    password = PasswordField(label='Пароль',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: auto; width: auto; ',
                         }
                         )
    submit = SubmitField("Войти",
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: auto; width: 40%; font-size: 14px'
                         }
                         )

class RegForm(FlaskForm):
    username = StringField(label='Имя пользователя',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: auto; width: auto; ',
                         }
                         )
    password = PasswordField(label='Пароль',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: auto; width: auto; ',
                         }
                         )
    password2 = PasswordField(label='Проверка пароля',
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: auto; width: auto; ',
                         }
                         )
    submit = SubmitField("Зарегистрироваться",
                         render_kw={
                             'class': 'form-control',
                             'style': 'height: auto; width: auto; font-size: 14px'
                         }
                         )