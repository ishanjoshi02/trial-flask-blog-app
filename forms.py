from flask_wtf import Form

from wtforms import StringField, PasswordField
from wtforms.validators import Email, DataRequired
from wtforms.widgets import PasswordInput


class RegisterForm(Form):
    firstname = StringField('firstname', validators=[
                            DataRequired(message="First name is required")])
    lastname = StringField('lastname', validators=[
                           DataRequired(message="Last name is required")])
    confirm_password = StringField(
        'confirm_password', validators=[DataRequired(message="Confirm Password is required")])
    username = StringField('username', validators=[
                           DataRequired(message="Username is required")])
    password = StringField('password', validators=[
                           DataRequired("Password is required")])


class LoginForm(Form):
    username = StringField("username", validators=[
                           DataRequired(message="username is required")])
    password = StringField("password", validators=[
                           DataRequired("password is required")], widget=PasswordInput())


class BlogForm(Form):
    title = StringField('title', validators=[
        DataRequired(message="Blog title is required")])
    content = StringField("content", validators=[
        DataRequired(message="Blog content is required")
    ])
