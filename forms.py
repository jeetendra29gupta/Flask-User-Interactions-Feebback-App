from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length, Email


class UserFeedbackForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=5, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    feedback = TextAreaField('Feedback', validators=[DataRequired(), Length(max=500)])
    submit = SubmitField('Submit')
