from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField, DateField
from wtforms.validators import DataRequired
from datetime import datetime

class ExpenseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    product = StringField('Product', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', default=datetime.today().date(), validators=[DataRequired()])
    submit = SubmitField('Submit')
