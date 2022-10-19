from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, HiddenField, TextAreaField


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