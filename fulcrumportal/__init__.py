from fulcrumportal.config import secret_key
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['CSRF_ENABLED'] = True
app.config['USER_ENABLE_EMAIL'] = False
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


from fulcrumportal import routes