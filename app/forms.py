from flask_wtf import FlaskForm
from wtforms import (StringField, SubmitField, FloatField,
                     PasswordField, BooleanField, SelectField)
from wtforms.validators import DataRequired, Email, NumberRange
from datetime import datetime

class ExpenseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])
    date = StringField('Date', validators=[DataRequired()])
    submit = SubmitField('Submit')



class IncomeForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    amount = FloatField('Amount', [DataRequired(), NumberRange(min=0, max=None, message="Amount must be a non-negative number.")])
    date = StringField('Date', [DataRequired()])
    frequency = SelectField('Frequency', choices=[('Daily', 'Daily'), ('Weekly', 'Weekly'), ('Monthly', 'Monthly'), ('Yearly', 'Yearly')], validators=[DataRequired()])
    submit = SubmitField('Submit')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Submit')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired()])
    submit = SubmitField('Register')