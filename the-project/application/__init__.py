# app/__init__.py

# third-party imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt




app = Flask(__name__)
app.config['SECRET_KEY'] = 'p9Bv<3Eid9%$i01'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)



from application import views
