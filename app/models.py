from flask_login import UserMixin

from app.extensions import db, bcrypt


class User(UserMixin, db.Model):
    """
    User model representing application users.

    Attributes:
        id (int): Primary key.
        username (str): Unique username.
        email (str): Unique email address.
        password_hash (str): Hashed password.
        image_file (str): Profile image filename.
        is_admin (bool): Flag for admin privileges.
        is_active (bool): Account active status.
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of last update.
        feedbacks (list): List of related Feedback instances.
    """

    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True, index=True)
    email = db.Column(db.String(120), nullable=False, unique=True, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    feedbacks = db.relationship(
        "Feedback", back_populates="user", cascade="all, delete-orphan"
    )

    def set_password(self, password: str) -> None:
        """
        Hash and set the user's password.

        Args:
            password (str): Plain text password.
        """
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    def check_password(self, password: str) -> bool:
        """
        Verify if provided password matches stored password hash.

        Args:
            password (str): Plain text password.

        Returns:
            bool: True if password matches, else False.
        """
        return bcrypt.check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return f"<User(username='{self.username}', email='{self.email}')>"


class Feedback(db.Model):
    """
    Feedback model representing user feedback entries.

    Attributes:
        id (int): Primary key.
        user_id (int): Foreign key to User.
        feedback (str): Text feedback content.
        status (str): Feedback status ('pending' by default).
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of last update.
        user (User): Related user object.
    """

    __tablename__ = "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    feedback = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="pending")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    user = db.relationship("User", back_populates="feedbacks")

    def __repr__(self) -> str:
        return f"<Feedback(user_id={self.user_id}, feedback='{self.id}...')>"
