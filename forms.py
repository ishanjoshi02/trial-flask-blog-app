from flask_wtf import Form

from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired


class RegisterForm(Form):
    firstname = StringField('firstname', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    confirm_password = StringField(
        'confirm_password', validators=[DataRequired()])
    username = StringField('username', validators=[DataRequired()])
    password = StringField('password', validators=[DataRequired()])


class LoginForm(Form):
    username = StringField("username", validators=[DataRequired()])
    password = StringField("password", validators=[DataRequired()])
