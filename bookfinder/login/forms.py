from wtforms import Form, TextField, PasswordField


class LoginForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')


class CreateUserForm(Form):
    username = TextField('Username')
    password = PasswordField('Password')
    verify_password = PasswordField('Verify Password')
