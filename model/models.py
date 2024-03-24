from datetime import datetime,timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from sqlalchemy.orm import validates
from app import db, login
from typing import Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash




# create expense model
class Expense(db.Model):
    __tablename__ = 'expenses'
    id : so.Mapped[int] = so.mapped_column(primary_key=True,nullable=False)
    name : so.Mapped[str] = so.mapped_column(sa.String(80), nullable=False, index=True)
    amount : so.Mapped[float] = so.mapped_column(sa.Float(), nullable=False)
    category : so.Mapped[str] = so.mapped_column(sa.String(80), nullable=False, index=True)
    date = so.mapped_column(sa.Date(),nullable=False, index=True)
    user_id: so.Mapped[int] = so.mapped_column(db.Integer, db.ForeignKey('user.id'))
    user: so.Mapped["User"] = so.relationship("User", back_populates='expenses')



    # def __init__(self, name, product, amount, category, date, user_id):
    #     self.name = name
    #     self.product = product
    #     self.amount = amount
    #     self.category = category
    #     self.date = date
    #     self.user_id = user_id

    def __repr__(self):
        return f'<Expense name={self.name} product={self.product} amount={self.amount} category={self.category} date={self.date} user_id={self.user_id} >'


class User(UserMixin, db.Model):
    __tablename__ = "user"
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
    incomes: so.Mapped["Income"] = so.relationship("Income", back_populates='user')
    expenses: so.Mapped["Expense"] = so.relationship("Expense", back_populates='user')

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return 'f<User {self.username}>'


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))


#aanmaak van de income klasse in de database
class Income(db.Model):
    __tablename__='incomes'
    id: so.Mapped[int] = so.mapped_column(sa.Integer, primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(80), nullable=False, index=True)
    amount: so.Mapped[int] = so.mapped_column(sa.Float, nullable=False)
    date = so.mapped_column(sa.Date(),nullable=False, index=True)
    frequency: so.Mapped[int] = so.mapped_column(sa.String(20), nullable=False)
    user_id: so.Mapped[int] = so.mapped_column(db.Integer, db.ForeignKey('user.id'))
    user: so.Mapped["User"] = so.relationship("User", back_populates='incomes')


