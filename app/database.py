from app import app, db
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from sqlalchemy import text
import os
import plotly.graph_objects as go
from jinja2 import Template
from model.models import Expense, Income
import sqlalchemy as sa
import plotly.express as px
import pandas


#plotly bekijken ipv matplotlib (handiger voor web) --> ook dash bekijken
def get_plot():
    with app.app_context():
        fig, ax = plt.subplots()
        x_pts = db.session.execute(text('SELECT product FROM expenses')).fetchall()
        y_pts = db.session.execute(text('SELECT amount FROM expenses')).fetchall()
        x_pts = [x[0] for x in x_pts]
        y_pts = [y[0] for y in y_pts]
        ax.plot(x_pts, y_pts, label='expenses')

        static_folder = app.static_folder
        filename = os.path.join(static_folder, 'plot.png')
        plt.savefig(filename)
        plt.close(fig)
        return filename




def get_data():
    with app.app_context():
        expense_name = [expense.name for expense in Expense.query.all()]
        expense_amount = [expense.amount for expense in Expense.query.all()]
        expense_date = [expense.date for expense in Expense.query.all()]
        income_name = [income.name for income in Income.query.all()]
        income_amount = [income.amount for income in Income.query.all()]
        income_frequency = [income.frequency for income in Income.query.all()]

        return expense_name, expense_amount, expense_date, income_name, income_amount, income_frequency




def get_figure():
    expense_name, expense_amount, expense_date, income_name, income_amount, income_frequency = get_data()
    with app.app_context():

        fig = go.Figure(data=[go.Bar(x=expense_name, y=expense_amount)])

        # Convert Plotly graph to HTML
        plot_html = fig.to_html(full_html=False)
        return plot_html

def get_figure_net_income():
    expense_name, expense_amount, expense_date, income_name, income_amount, income_frequency = get_data()
    print(expense_amount, income_amount)
    income = sum(income_amount)
    outflow = sum(expense_amount)

    net_income = income - outflow


    with app.app_context():
        fig_net_income = go.Figure(data=[go.Bar(x=income_amount, y=net_income)])

        # Convert Plotly graph to HTML
        plotaa_html = fig_net_income.to_html(full_html=False)
        return plotaa_html


def get_figure_three():

    pass