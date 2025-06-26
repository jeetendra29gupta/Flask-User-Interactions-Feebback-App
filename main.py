from datetime import datetime, timezone
from logging import DEBUG

from flask import Flask, render_template, request, redirect, url_for, flash

from forms import UserFeedbackForm

# --- Flask App Setup ---
app = Flask(__name__)
app.secret_key = 'my-secret-key'

# --- Logging Configuration ---
app.logger.setLevel(DEBUG)

# --- In-Memory Storage for Feedback ---
feedbacks = []


def store_feedback(data):
    feedbacks.append({
        "Created At": datetime.now(tz=timezone.utc).isoformat(),
        "User Name": data.get('username'),
        "Email ID": data.get('email'),
        "Feedback": data.get('feedback')
    })


# --- Routes ---
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/feedback', methods=['GET', 'POST'])
def feedback():
    form = UserFeedbackForm()
    if form.validate_on_submit():
        feedback_data = {
            'username': form.username.data,
            'email': form.email.data,
            'feedback': form.feedback.data
        }
        store_feedback(feedback_data)
        flash('Feedback submitted successfully.', 'success')
        return redirect(url_for('feedback'))

    if request.method == 'POST':
        flash('Please correct the errors in the form.', 'danger')

    return render_template('feedback.html', form=form, feedbacks=feedbacks)


@app.errorhandler(404)
def page_not_found(error):
    app.logger.error(f"404 error: {error}")
    return render_template('404.html', error=error), 404


if __name__ == '__main__':
    app.logger.info("Starting the Flask application")
    app.run(host='0.0.0.0', port=8181, debug=True, )
