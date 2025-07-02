from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()
login_manager = LoginManager()

login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"
