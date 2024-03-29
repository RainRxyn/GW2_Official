import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from model.models import Expense

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'model': db, 'Expense': Expense}

if __name__ == '__main__':
    app.run(debug=True)
