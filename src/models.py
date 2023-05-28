"""Module with database models"""
import enum
# Import flask_login
from flask_login import UserMixin
# Import SQLAlchemy
from sqlalchemy import Column, Integer, String, Text, ForeignKey
# Import password / encryption helper tools
from werkzeug.security import generate_password_hash, check_password_hash
from . import db


class Users(db.Model, UserMixin):
    """User model for sqlalchemy database"""

    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column(String(20), nullable=False, unique=True)
    email = Column(String(20), nullable=False, unique=True)
    password_hash = Column(String(128))
    profile_picture = Column(String(), nullable=False, default="default_pic.jpg")
    data_created = Column(db.DateTime, default=db.func.current_timestamp())
    posts = db.relationship("Posts", backref="author", lazy=True)
    comments = db.relationship("Comments", backref="author", lazy=True)
    likes = db.relationship("PostsLikes", backref="author", lazy=True)

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
    comments = db.relationship("Comments", backref="post", lazy=True)
    likes = db.relationship("PostsLikes", backref="post", lazy=True)

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


class Comments(db.Model):
    """Comments model for sqlalchemy database"""

    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    # Foreign key to Posts
    post_id = Column(Integer, ForeignKey("posts.id"))
    # Foreign key to Users
    author_id = Column(Integer, ForeignKey("users.id"))
    comment = Column(Text, nullable=False)
    date_added = Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"Comment {self.comment} by {self.author} on post {self.post_id}"


class PostsLikes(db.Model):
    """Posts likes model for sqlalchemy database"""

    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    # Foreign key to Posts
    post_id = Column(Integer, ForeignKey("posts.id"))
    # Foreign key to Users
    author_id = Column(Integer, ForeignKey("users.id"))
    date_liked = Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"User {self.author_id} liked post {self.post_id}"


class relationship_status(enum.Enum):
    """Enum for relationship status"""

    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"


class Relationship(db.Model):
    """Relationship model for sqlalchemy database"""

    _id = Column("id", Integer, primary_key=True, autoincrement=True)
    # Foreign key to Users
    user_a_id = Column(Integer, ForeignKey("users.id"))
    # Foreign key to Users
    user_b_id = Column(Integer, ForeignKey("users.id"))
    status = Column(db.Enum(relationship_status), default=relationship_status.pending, nullable=False)
    date_added = Column(db.DateTime, default=db.func.current_timestamp())

    user_a = db.relationship("Users", foreign_keys=[user_a_id], backref="user_a")
    user_b = db.relationship("Users", foreign_keys=[user_b_id], backref="user_b")

    def __repr__(self):
        return f"User {self.user_a.name} is friends with {self.user_b.name}"
