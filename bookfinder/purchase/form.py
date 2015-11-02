from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, DecimalField
from wtforms.validators import DataRequired

class LoginForm(Form):
    ISBN = StringField('ISBN', validators=[DataRequired()])
    Price = DecimalField('Price', validators=[DataRequired()])
    Title = StringField('Title', validators=[DataRequired()])
    Author = StringField('Author', validators = [DataRequired()])
