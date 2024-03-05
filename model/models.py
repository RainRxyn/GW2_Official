from datetime import datetime, timezone
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login
from typing import Optional
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


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


class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def set_password(self, password: str):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))