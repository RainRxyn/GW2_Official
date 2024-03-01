from datetime import datetime,timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db

# create expense model
class Expense(db.Model):
    __tablename__ = 'expenses'
    id : so.Mapped[int] = so.mapped_column(primary_key=True,nullable=False)
    name : so.Mapped[str] = so.mapped_column(sa.String(80), nullable=False,
                                             index=True)
    product : so.Mapped[str] = so.mapped_column(sa.String(80), nullable=False)
    amount : so.Mapped[float] = so.mapped_column(sa.Float(), nullable=False)
    category : so.Mapped[str] = so.mapped_column(sa.String(80), nullable=False,
                                                 index=True)




    def __init__(self, name, product, amount, category):
        self.name = name
        self.product = product
        self.amount = amount
        self.category = category

    def __repr__(self):
        return f'<Expense name={self.name} product={self.product} amount={self.amount} category={self.category}>'


