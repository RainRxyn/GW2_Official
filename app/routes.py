from flask import render_template, flash, redirect, request
from app import app,db
from app.forms import ExpenseForm, IncomeForm
from model.models import Expense, Income
from datetime import datetime



@app.route('/')
@app.route('/index')
def index():
    form_expense = ExpenseForm()
    return render_template('index.html',form=form_expense)



@app.route('/add_expense', methods=['POST','GET'])
def add_expense():
    form_expense = request.form
    if request.method == 'POST':
        name = form_expense['name']
        product = form_expense['product']
        amount = form_expense['amount']
        category = form_expense['category']

        try:
            db.session.add(Expense(name=name,
                                   product=product,
                                   amount=amount,
                                   category=category))
            db.session.commit()
            flash('Expense added successfully!', 'success')
        except:
            db.session.rollback()
            flash('Failed to add expense. Please try again.', 'danger')
        return redirect('/add_expense')
    return render_template('add_expenses.html')

@app.route('/show_expenses' , methods=['GET','POST'])
def show_expenses():
    expenses = db.session.query(Expense).all()
    return render_template('show_expenses.html', expenses=expenses)




@app.route('/delete_expenses', methods=['POST'])
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

                db.session.commit()
                flash('Expense updated successfully!', 'success')
            except:
                db.session.rollback()
                flash('Failed to update expense. Please try again.', 'danger')

        else:
            flash('Expense not found.', 'danger')

    return redirect('/show_expenses')


@app.route('/add_income', methods=["POST", "GET"])
def add_income():
    if request.method == 'POST':
        form_income = request.form
        name = form_income['name']
        amount = form_income['amount']
        frequency = form_income['frequency']

        try:
            db.session.add(Income(name=name,
                                  amount=amount,
                                  frequency=frequency))
            db.session.commit()
            flash("Income has succesfully been added")

        except Exception as e:
            db.session.rollback()
            flash(f"Failed to update income, {e}")
        return redirect('/add_income')
    return render_template('add_income.html')
