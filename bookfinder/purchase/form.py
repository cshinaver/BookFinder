from flask.ext.wtf import Form
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired

class LoginForm(Form):
    ISBN = StringField('ISBN', validators=[DataRequired()])
    Price = StringField('Price', validators=[DataRequired()])
