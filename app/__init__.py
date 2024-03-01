from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__, template_folder="../view")
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


app.config['SECRET_KEY'] = 'you-will-never-guess'

from app import routes, errors
