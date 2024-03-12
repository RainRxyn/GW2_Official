from flask import render_template, flash, redirect, request, url_for
from urllib.parse import urlsplit
from app import app, db
from app.forms import ExpenseForm, LoginForm, RegisterForm
from model.models import Expense, Income, User
from flask_login import login_user, logout_user, login_required, current_user
import sqlalchemy as sa
from sqlalchemy import text
from datetime import datetime


@app.route('/')
@app.route('/index')
def index():
    form_expense = ExpenseForm()
    return render_template('index.html',form=form_expense)


@app.route('/add_expense', methods=['POST', 'GET'])
@login_required
def add_expense():
    form_expense = request.form
    if request.method == 'POST':
        name = form_expense['name']
        product = form_expense['product']
        amount = form_expense['amount']
        category = form_expense['category']
        date = form_expense['date']
        user_id = current_user.id

        try:

            date = datetime.strptime(date,'%Y-%m-%d')
            db.session.add(Expense(name=name,
                                   product=product,
                                   amount=amount,
                                   category=category,
                                   date=date,
                                   user_id=user_id))

            db.session.commit()
            flash('Expense added successfully!', 'success')

        except:
            db.session.rollback()
            flash('Failed to add expense. Please try again.', 'danger')
        return redirect('/add_expense')
    return render_template('add_expenses.html')


@app.route('/show_expenses' , methods=['GET','POST'])
@login_required
def show_expenses():
    expenses = db.session.execute(text('SELECT * FROM expenses')).fetchall()
    return render_template('show_expenses.html', expenses=expenses)


@app.route('/delete_expenses', methods=['POST'])
@login_required
def delete_expenses():
    if request.method == 'POST':
        id = request.form['id']
        expense = Expense.query.get(id)
        try:
            db.session.delete(expense)
            db.session.commit()
            flash('Expense deleted successfully!', 'success')
        except:
            db.session.rollback()
            flash('Failed to delete expense. Please try again.', 'danger')
        return redirect('/show_expenses')


@app.route('/edit_expenses/<int:id>', methods=['POST'])
@login_required
def edit_expenses(id):
    if request.method == 'POST':
        expense = Expense.query.get(id)
        if expense:
            try:
                if 'name' in request.form and request.form['name']:
                    expense.name = request.form['name']
                if 'product' in request.form and request.form['product']:
                    expense.product = request.form['product']
                if 'amount' in request.form and request.form['amount']:
                    expense.amount = request.form['amount']
                if 'category' in request.form and request.form['category']:
                    expense.category = request.form['category']
                if 'date' in request.form and request.form['date']:
                    expense.date = datetime.strptime(request.form['date'], '%Y-%m-%d')


                db.session.commit()
                flash('Expense updated successfully!', 'success')
            except:
                db.session.rollback()
                flash('Failed to update expense. Please try again.', 'danger')

        else:
            flash('Expense not found.', 'danger')

    return redirect('/show_expenses')


@app.route('/add_income', methods=["POST", "GET"])
@login_required
def add_income():
    if request.method == 'POST':
        form_income = request.form
        name = form_income['name']
        amount = form_income['amount']
        frequency = form_income['frequency']
        user_id = current_user.id

        try:
            db.session.add(Income(name=name,
                                  amount=amount,
                                  frequency=frequency,
                                  user_id= user_id))
            db.session.commit()
            flash("Income has succesfully been added")

        except Exception as e:
            db.session.rollback()
            flash(f"Failed to update income, {e}")
        return redirect('/add_income')
    return render_template('add_income.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))

        if user is None or not user.check_password(form.password.data):
            flash('Invalid email address or password')
            return redirect(url_for('login'))

        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')

        return redirect(next_page)

    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm()

    if form.validate_on_submit():

        user = db.session.scalar(sa.select(User).where(User.email == form.email.data))

        if form.password.data == form.password2.data:

            if user is None:

                user = User(email=form.email.data, username=form.username.data)
                user.set_password(form.password.data)
                db.session.add(user)
                db.session.commit()
                flash('You are a registered user. Please login')
                return redirect(url_for('login'))

            else:
                flash('This email is already in use')

        else:
            flash('The passwords do not match')

    return render_template('register.html', title='Register', form=form)


@app.route('/filter_expenses', methods=['GET', 'POST'])
@login_required
def filter_expenses():
    if request.method == 'POST':
        form = request.form
        name = form.get('name', None)
        if name:
            expenses =  db.session.execute(text('SELECT * FROM expenses WHERE name LIKE :search_name'),{'search_name': f'{name}%'}).fetchall()
            if expenses:
                flash('Expense name found', 'success')
            else:
                expenses = db.session.execute(text('SELECT * FROM expenses')).fetchall()
                flash('Expense name not found', 'danger')
        else:
            expenses = db.session.execute(text('SELECT * FROM expenses'))
            flash('Please enter a name', 'danger')
    if request.args.get('category') == 'asc':
        expenses = db.session.execute(text('SELECT * FROM expenses ORDER BY category ASC'))
    if request.args.get('category') == 'desc':
        expenses = db.session.execute(text('SELECT * FROM expenses ORDER BY category DESC'))
    if request.args.get('date') == 'date_asc':
        expenses = db.session.execute(text('SELECT * FROM expenses ORDER BY date ASC'))
    if request.args.get('date') == 'date_desc':
        expenses = db.session.execute(text('SELECT * FROM expenses ORDER BY date DESC'))

    return render_template('show_expenses.html', expenses=expenses)







