import pytest

from app.models import User, Feedback


def test_user_creation(db_session):
    user = User(username="testuser", email="test@example.com")
    user.set_password("securepassword")
    db_session.add(user)
    db_session.commit()


def test_user_properties(db_session):
    retrieved_user = User.query.filter_by(email="test@example.com").first()
    assert retrieved_user is not None
    assert retrieved_user.username == "testuser"
    assert retrieved_user.check_password("securepassword")
    assert not retrieved_user.check_password("wrongpassword")
    assert retrieved_user.image_file == "default.jpg"
    assert retrieved_user.is_active is True
    assert retrieved_user.is_admin is False


def test_feedback_creation(db_session):
    retrieved_user = User.query.filter_by(email="test@example.com").first()
    feedback = Feedback(user_id=retrieved_user.id, feedback="Great app experience!")
    db_session.add(feedback)
    db_session.commit()


def test_feedback_relationship(db_session):
    feedback = Feedback.query.first()
    user = User.query.first()
    assert feedback is not None
    assert feedback.user.username == "testuser"
    assert feedback.status == "pending"
    assert len(user.feedbacks) == 1
    assert user.feedbacks[0].feedback == "Great app experience!"


if __name__ == "__main__":
    pytest.main(["-v", __file__])
