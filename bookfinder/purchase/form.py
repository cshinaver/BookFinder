from flask.ext.wtf import Form
from wtforms import StringField, DecimalField
from wtforms.validators import DataRequired


class SellBookForm(Form):
    ISBN = StringField('ISBN', validators=[DataRequired()])
    Price = DecimalField('Price', validators=[DataRequired()])
