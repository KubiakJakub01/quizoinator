"""Module with database models"""
from . import db
# Import flask_login
from flask_login import UserMixin
# Import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey
# Import password / encryption helper tools
from werkzeug.security import generate_password_hash, check_password_hash


class Users(db.Model, UserMixin):
    """User model for sqlalchemy database"""

    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    email = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String(128))
    data_created = Column(db.DateTime, default=db.func.current_timestamp())
    posts = db.relationship("Posts", backref="author", lazy=True)

    @property
    def password(self):
        """Prevent password from being accessed"""
        raise AttributeError("Password is not a readable attribute")

    @password.setter
    def password(self, password):
        """Set password to a hashed password"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """Check if hashed password matches actual password"""
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        """Return id"""
        return self._id

    def __repr__(self):
        return self.name


class Posts(db.Model):
    """Posts model for sqlalchemy database"""

    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, unique=True)
    content = Column(Text, nullable=False, unique=True)
    data_created = Column(db.DateTime, default=db.func.current_timestamp())
    # Foreign key to Users
    author_id = Column(Integer, ForeignKey("users.id"))

    def __repr__(self):
        return f"Post {self.title} with content {self.content}"


class Admin(db.Model):
    """Admin model for sqlalchemy database"""

    admin_id = Column("id", Integer, primary_key=True, autoincrement=True)
    # Foreign key to Users
    user_id = Column(Integer, ForeignKey("users.id"))
    # Foreign key to person who added admin
    added_by = Column(Integer, ForeignKey("users.id"))
    # reason for adding admin
    reason = Column(String(200), nullable=False)
    # Date admin was added
    date_added = Column(db.DateTime, default=db.func.current_timestamp())
