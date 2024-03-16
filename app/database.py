from app import app, db
import numpy as np
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
from sqlalchemy import text
import os



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


