import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    EXPENSES_PER_PAGE = 5
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:ww01@localhost:5432/app.db'
