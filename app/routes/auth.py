from flask import Blueprint, redirect, url_for, flash, render_template, request
from flask_login import current_user, login_user, login_required, logout_user

from app.extensions import db
from app.forms import SignupForm, LoginForm, FeedbackForm
from app.logger import setup_logger
from app.models import User, Feedback

auth = Blueprint("auth", __name__)
logger = setup_logger(__name__)


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        logger.info("User is already authenticated, redirecting to index.")
        return redirect(url_for("main.index"))

    form = SignupForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data)
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        logger.info(f"New user created: {new_user.username}")
        flash("Account created! You are now logged in.", "success")
        login_user(new_user)
        return redirect(url_for("main.index"))

    return render_template("signup.html", form=form, user=None)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        logger.info("User is already authenticated, redirecting to index.")
        return redirect(url_for("main.index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            logger.info(f"User logged in: {user.username}")
            flash("Login successful!", "success")
            next_page = request.args.get("next")
            return redirect(next_page or url_for("main.index"))
        else:
            logger.warning(f"Invalid login attempt: {form.email.data}")
            flash("Invalid username or password.", "danger")

    return render_template("login.html", form=form, user=None)


@auth.route("/logout")
@login_required
def logout():
    username = current_user.username
    logout_user()
    logger.info(f"User logged out: {username}")
    flash("You have been logged out.", "success")
    return redirect(url_for("main.index"))


@auth.route("/feedback", methods=["GET", "POST"])
@login_required
def feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        user_feedback = Feedback(user_id=current_user.id, feedback=form.feedback.data)
        db.session.add(user_feedback)
        db.session.commit()
        logger.info(f"Feedback submitted by user: {current_user.username}")
        flash("Feedback submitted successfully!", "success")
        return redirect(url_for("auth.feedback"))

    if request.method == "POST":
        logger.warning("Feedback form submission failed validation.")
        flash("Please correct the errors in the form.", "danger")

    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).all()
    return render_template(
        "feedback.html", form=form, feedbacks=feedbacks, user=current_user
    )
