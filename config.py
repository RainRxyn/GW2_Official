import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    EXPENSES_PER_PAGE = 5
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgres://postgres:postgres@localhost:5432/expenses'
