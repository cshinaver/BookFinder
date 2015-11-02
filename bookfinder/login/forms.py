from wtforms import Form, TextField, PasswordField


class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')
