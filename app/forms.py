import re
from typing import Any

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, ValidationError, EqualTo

from app.models import User


def validate_username(form: FlaskForm, field: Any) -> None:
    """
    Custom validator to check if username already exists in DB.

    Args:
        form (FlaskForm): The form instance.
        field (Any): The field being validated.

    Raises:
        ValidationError: If username already exists.
    """
    if User.query.filter_by(username=field.data).first():
        raise ValidationError("Username already exists.")


def validate_email(form: FlaskForm, field: Any) -> None:
    """
    Custom validator to check if email is already registered.

    Args:
        form (FlaskForm): The form instance.
        field (Any): The field being validated.

    Raises:
        ValidationError: If email is already registered.
    """
    if User.query.filter_by(email=field.data).first():
        raise ValidationError("Email already registered.")


def validate_password(form: FlaskForm, field: Any) -> None:
    """
    Custom password complexity validator.

    Password must contain at least:
    - One uppercase letter
    - One lowercase letter
    - One digit
    - One special character

    Args:
        form (FlaskForm): The form instance.
        field (Any): The password field.

    Raises:
        ValidationError: If any complexity rule is not met.
    """
    password = field.data
    if not re.search(r"[A-Z]", password):
        raise ValidationError("Password must include at least one uppercase letter.")
    if not re.search(r"[a-z]", password):
        raise ValidationError("Password must include at least one lowercase letter.")
    if not re.search(r"\d", password):
        raise ValidationError("Password must include at least one number.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValidationError("Password must include at least one special character.")


class SignupForm(FlaskForm):
    """
    User signup form with validation.

    Fields:
        username (str): Username, unique.
        email (str): Email address, unique.
        password (str): Password with complexity requirements.
        confirm_password (str): Must match password.
        submit (submit): Submit button.
    """

    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=3, max=50), validate_username],
    )
    email = StringField(
        "Email", validators=[DataRequired(), Email(), Length(max=120), validate_email]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=8), validate_password]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Sign Up")


class LoginForm(FlaskForm):
    """
    User login form.

    Fields:
        email (str): User's registered email.
        password (str): Password.
        submit (submit): Submit button.
    """

    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=120)])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class FeedbackForm(FlaskForm):
    """
    User feedback submission form.

    Fields:
        feedback (str): User's feedback text.
        submit (submit): Submit button.
    """

    feedback = TextAreaField(
        "Your Feedback", validators=[DataRequired(), Length(min=5)]
    )
    submit = SubmitField("Submit")
