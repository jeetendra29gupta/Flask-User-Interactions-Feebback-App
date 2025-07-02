from flask import Flask, render_template

from app.config import current_config
from app.extensions import db, bcrypt, cors, login_manager
from app.logger import setup_logger
from app.models import User
from app.routes import main, auth

# -----------------------------------------------------
# 🌱 Application Setup (Factory Pattern Style)
# -----------------------------------------------------

app = Flask(__name__)
app.config.from_object(current_config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
cors.init_app(app)
login_manager.init_app(app)


# -----------------------------------------------------
# 🔐 User Session Management with Flask-Login
# -----------------------------------------------------


@login_manager.user_loader
def load_user(user_id):
    """Load user from session using user_id."""
    return User.query.get(int(user_id))


login_manager.login_view = "auth.login"
login_manager.login_message_category = "info"


# -----------------------------------------------------
# 🌐 Error Handlers
# -----------------------------------------------------


@app.errorhandler(404)
def not_found_error(error):
    app.logger.error(f"404 error: {error}")
    return render_template("error.html", code=404, message="Oops! Page not found."), 404


# -----------------------------------------------------
# 📦 Blueprint Registration
# -----------------------------------------------------

app.register_blueprint(main.main, url_prefix="/")
app.register_blueprint(auth.auth, url_prefix="/")


# -----------------------------------------------------
# 🚀 App Entry Point
# -----------------------------------------------------


def main():
    logger = setup_logger(__name__)
    logger.info(f"Starting application in {current_config.APP_ENV} mode")
    app.run(
        host=current_config.HOST, port=current_config.PORT, debug=current_config.DEBUG
    )


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        main()
