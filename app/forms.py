from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, FloatField
from wtforms.validators import DataRequired

class ExpenseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    product = StringField('Product', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    submit = SubmitField('Submit')
