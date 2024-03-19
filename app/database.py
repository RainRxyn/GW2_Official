from app import app, db
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from sqlalchemy import text
import os
import plotly.graph_objects as go
from jinja2 import Template
from model.models import Expense
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
        return expense_name, expense_amount, expense_date


get_data()


def get_figure():
    expense_name, expense_amount, expense_date = get_data()
    with app.app_context():

        fig = go.Figure(data=[go.Bar(x=expense_name, y=expense_amount)])

        # Convert Plotly graph to HTML
        plot_html = fig.to_html(full_html=False)
        return plot_html
