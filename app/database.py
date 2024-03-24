from app import app, db
import matplotlib as mpl
import matplotlib.pyplot as plt
from sqlalchemy import text
import os
import plotly.graph_objects as go
from model.models import Expense, Income
mpl.use('Agg')





def get_data():
    # Retrieve all the data from db
    with app.app_context():
        expense_name = [expense.name for expense in Expense.query.all()]
        expense_amount = [expense.amount for expense in Expense.query.all()]
        expense_date = [expense.date for expense in Expense.query.all()]
        income_name = [income.name for income in Income.query.all()]
        income_amount = [income.amount for income in Income.query.all()]
        income_frequency = [income.frequency for income in Income.query.all()]
        income_date = [income.date for income in Income.query.all()]

        return expense_name, expense_amount, expense_date, income_name, income_amount, income_frequency, income_date


def get_figure():
    expense_name, expense_amount, expense_date, income_name, income_amount, income_frequency, income_date = get_data()
    with app.app_context():

        fig = go.Figure(data=[go.Bar(x=expense_name, y=expense_amount)])
        fig.update_layout(title='Expenses',
                          xaxis_title='Expense',
                          yaxis_title='Expense Name')

        # Convert Plotly graph to HTML
        plot_html = fig.to_html(full_html=False)
        return plot_html


def get_figure_net_income():
    expense_name, expense_amount, expense_date, income_name, income_amount, income_frequency, income_date = get_data()

    # Aggregate income by month using the provided function
    net_income_by_month = aggregate_income_by_month(income_date, income_amount, expense_date, expense_amount)

    months = list(net_income_by_month.keys())
    net_income = list(net_income_by_month.values())

    if len(months) == 1:
        months.append('')  # Adds placeholder for if there's only one month

    with app.app_context():
        # Create the bar chart
        fig_net_income = go.Figure(data=[go.Bar(x=months, y=net_income)])

        # Add labels and title
        fig_net_income.update_layout(
            title="Net Income Per Month",
            xaxis_title="Month",
            yaxis_title="Net Income"
        )

        # Convert Plotly graph to HTML
        plotaa_html = fig_net_income.to_html(full_html=False)
        return plotaa_html


def aggregate_income_by_month(income_date, income_amount, expense_date, expense_amount):
    from collections import defaultdict
    from datetime import datetime

    income_by_month = defaultdict(float)
    for date, amount in zip(income_date, income_amount):
        month = date.strftime("%Y-%m")
        income_by_month[month] += amount

    # Convert expense_date to strings to make comparing possible
    expense_date_strings = [date.strftime("%Y-%m-%d") for date in expense_date]

    # Calculate net income per month
    net_income_by_month = {}
    for month, income in income_by_month.items():
        outflow = sum(amount for date, amount in zip(expense_date_strings, expense_amount) if
                      datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m") == month)
        net_income_by_month[month] = income - outflow

    return net_income_by_month


