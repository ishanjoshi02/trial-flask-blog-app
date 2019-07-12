from flask_wtf import Form

from wtforms import StringField, PasswordField
from wtforms.validators import EqualTo, DataRequired
from wtforms.widgets import PasswordInput


class RegisterForm(Form):
    firstname = StringField('firstname', validators=[
                            DataRequired(message="First name is required")])
    lastname = StringField('lastname', validators=[
                           DataRequired(message="Last name is required")])
    username = StringField('username', validators=[
                           DataRequired(message="Username is required")])
    password = PasswordField('Password', validators=[
        DataRequired("Password is required"), EqualTo("confirm_password",  message='Passwords must match')])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(message="Confirm Password is required")])


class LoginForm(Form):
    username = StringField("username", validators=[
                           DataRequired(message="username is required")])
    password = PasswordField("Password", validators=[
        DataRequired("password is required")])


class BlogForm(Form):
    title = StringField('title', validators=[
        DataRequired(message="Blog title is required")])
    content = StringField("content", validators=[
        DataRequired(message="Blog content is required")
    ])
