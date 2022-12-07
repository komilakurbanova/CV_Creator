from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import os

DATABASE = 'database'

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True
app.config['SECRET_KEY'] = 'secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, '%s.db' % DATABASE)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message = "Authorize for further work"
login_manager.login_message_category = "success"
login_manager.init_app(app)

db.init_app(app)

from auth import auth as auth_blueprint

app.register_blueprint(auth_blueprint)

from main import main as main_blueprint

app.register_blueprint(main_blueprint)

if __name__ == "__main__":
    app.run(debug=DEBUG)