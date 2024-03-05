import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from typing import Optional


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
    date = so.mapped_column(sa.Date(), index=True)

    def __init__(self, name, product, amount, category, date):
        self.name = name
        self.product = product
        self.amount = amount
        self.category = category
        self.date = date



    def __repr__(self):
        return f'<Expense name={self.name} product={self.product} amount={self.amount} category={self.category} >'


class User(db.Model):
    __tablename__ = "user"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))


    def __repr__(self):
        return '<User {}>'.format(self.username)