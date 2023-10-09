from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, BooleanField, SubmitField, SelectField, RadioField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = SelectField('Выберите пользователь', choices=[], validators=[DataRequired()])
    password = PasswordField('Введите пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запонить меня', default=True)
    submit = SubmitField('Войти')


class AuthForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    role = SelectField('Права', choices=['admin', 'skud', 'operator', 'all'])
    submit = SubmitField('Добавить пользователя')


class EditUserForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()])
    password = StringField('Пароль', validators=[DataRequired()])
    role = SelectField('Права', choices=['admin', 'skud', 'operator', 'all'])
    submit = SubmitField('Сохранить')
