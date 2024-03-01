from flask import render_template, flash, redirect, request
from app import app,db
from app.forms import ExpenseForm
from model.models import Expense



@app.route('/')
@app.route('/index')
def index():
    form = ExpenseForm()
    return render_template('index.html',form=form)



@app.route('/add_expense', methods=['POST','GET'])
def add_expense():
    form = request.form
    if request.method == 'POST':
        name = form['name']
        product = form['product']
        amount = form['amount']
        category = form['category']

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
