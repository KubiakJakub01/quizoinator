"""Script to feed the database with sample data"""
import shutil
import argparse
from pathlib import Path
from random import randint, choice

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from src.models import Users, Posts, Admin, Comments, PostsLikes, Relationship



def get_params():
    parser = argparse.ArgumentParser(description="Feed the database with sample data")
    parser.add_argument(
        "--db_url",
        type=str,
        default="instance/database.db",
        help="Path to the database file",
    )
    parser.add_argument(
        "-p",
        "--pictures_dir",
        type=Path,
        default="pictures",
        help="Directory containing the profile pictures",
    )
    parser.add_argument(
        "-s",
        "--pictures_save_dir",
        type=Path,
        default="src/static/user/images",
        help="Directory to save the profile pictures",
    )
    parser.add_argument(
        "--posts_num",
        type=int,
        default=10,
        help="Number of posts to create",
    )
    parser.add_argument(
        "--comments_num",
        type=int,
        default=30,
        help="Number of comments to create",
    )
    parser.add_argument(
        "--likes_num",
        type=int,
        default=50,
        help="Number of likes to create",
    )
    parser.add_argument(
        "--relationships_num",
        type=int,
        default=20,
        help="Number of relationships to create",
    )
    return parser.parse_args()


def create_sample_users(pictures_dir: Path):
    """Create sample users"""
    users = [
        {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "profile_picture": pictures_dir / "p1.PNG",
        },
        {
            "name": "Jane Smith",
            "email": "jane@example.com",
            "password": "pass456",
            "profile_picture": pictures_dir / "p2.PNG",
        },
        {
            "name": "Bob Johnson",
            "email": "bob@example.com",
            "password": "pass789",
            "profile_picture": pictures_dir / "p3.PNG",
        },
        {
            "name": "Alice Williams",
            "email": "alice@example.com",
            "password": "pass101112",
            "profile_picture": pictures_dir / "p4.PNG",
        },
        {
            "name": "Michael Brown",
            "email": "michael@example.com",
            "password": "pass131415",
            "profile_picture": pictures_dir / "p5.PNG",
        },
        {
            "name": "Patricia Jones",
            "email": "patricia@example.com",
            "password": "pass161718",
            "profile_picture": pictures_dir / "p6.PNG",
        },
        {
            "name": "David Miller",
            "email": "david@example.com",
            "password": "pass192021",
            "profile_picture": pictures_dir / "p7.PNG",
        },
        {
            "name": "Linda Davis",
            "email": "linda@example.com",
            "password": "pass222324",
            "profile_picture": pictures_dir / "p8.PNG",
        },
        {
            "name": "Susan Wilson",
            "email": "susan@example.com",
            "password": "pass252627",
            "profile_picture": pictures_dir / "p9.PNG",
        },
        {
            "name": "Richard Taylor",
            "email": "richard@example.com",
            "password": "pass282930",
            "profile_picture": pictures_dir / "p10.PNG",
        },
    ]
    return users


def submit_users(session, users: list, pictures_save_dir: Path):
    """Add users to the database"""
    def _process_picture(picture: Path):
        """Process picture"""
        profile_filename = secure_filename(picture.name)
        pic_name = profile_filename
        if pictures_save_dir / pic_name != picture:
            shutil.copy(str(picture), str(pictures_save_dir / pic_name))
        return pic_name
    for user in users:
        new_user = Users(
            name=user["name"],
            email=user["email"],
            password_hash=generate_password_hash(user["password"]),
            profile_picture=_process_picture(user["profile_picture"])
        )
        session.add(new_user)
    session.commit()


def create_sample_posts(users_num: int, posts_num: int):
    """Create sample posts"""
    posts = []
    for i in range(posts_num):
        posts.append(
            {
                "title": f"Post {i+1}",
                "content": f"This is the content of post {i+1}.",
                "author_id": randint(1, users_num)
            }
        )
    return posts


def submit_posts(session, posts: list):
    """Add posts to the database"""
    for post in posts:
        new_post = Posts(
            title=post["title"],
            content=post["content"],
            author_id=post["author_id"],
        )
        session.add(new_post)
    session.commit()


def create_sample_admins():
    """Create sample admins"""
    admins = [
        {
            "user_id": 1,
            "added_by": 2,
            "reason": "For administrative purposes.",
        },
    ]
    return admins

def submit_admins(session, admins: list):
    """Add admins to the database"""
    for admin in admins:
        new_admin = Admin(
            user_id=admin["user_id"],
            added_by=admin["added_by"],
            reason=admin["reason"],
        )
        session.add(new_admin)
    session.commit()


def create_sample_comments(users_num: int, posts_num: int, comments_num: int):
    """Create sample comments"""
    comments = []
    for i in range(comments_num):
        comments.append(
            {
                "post_id": randint(1, posts_num),
                "author_id": randint(1, users_num),
                "comment": f"This is comment {i+1}.",
            }
        )
    return comments


def submit_comments(session, comments: list):
    """Add comments to the database"""
    for comment in comments:
        new_comment = Comments(
            post_id=comment["post_id"],
            author_id=comment["author_id"],
            comment=comment["comment"],
        )
        session.add(new_comment)
    session.commit()


def create_sample_post_likes(users_num: int, posts_num: int, likes_num: int):
    """Create sample post likes"""
    post_likes = []
    for i in range(likes_num):
        post_likes.append(
            {
                "post_id": randint(1, posts_num),
                "author_id": randint(1, users_num),
            }
        )
    return post_likes


def submit_post_likes(session, post_likes: list):
    """Add post likes to the database"""
    for post_like in post_likes:
        new_post_like = PostsLikes(
            post_id=post_like["post_id"],
            author_id=post_like["author_id"],
        )
        session.add(new_post_like)
    session.commit()


def create_sample_relationships(users_num: int, relationships_num: int):
    """Create sample relationships"""
    relationships = []
    ralationship_status = ["pending", "accepted", "rejected"]
    for _ in range(relationships_num):
        relationships.append(
            {
                "user_a_id": randint(1, users_num),
                "user_b_id": randint(1, users_num),
                "status": choice(ralationship_status),
            }
        )
    return relationships


def submit_relationships(session, relationships: list):
    """Add relationships to the database"""
    for relationship in relationships:
        new_relationship = Relationship(
            user_a_id=relationship["user_a_id"],
            user_b_id=relationship["user_b_id"],
            status=relationship["status"],
        )
        session.add(new_relationship)
    session.commit()

if __name__ == "__main__":
    # Get parameters
    args = get_params()

    # Create a database connection
    engine = create_engine(f"sqlite:///{args.db_url}")
    Session = sessionmaker(bind=engine)
    session = Session()

    # Users
    users = create_sample_users(args.pictures_dir)
    submit_users(session, users, args.pictures_save_dir)

    # Posts
    posts = create_sample_posts(len(users), 10)
    submit_posts(session, posts)

    # Admins
    admins = create_sample_admins()
    submit_admins(session, admins)

    # Comments
    comments = create_sample_comments(len(users), len(posts), args.comments_num)
    submit_comments(session, comments)

    # Post likes
    post_likes = create_sample_post_likes(len(users), len(posts), args.likes_num)
    submit_post_likes(session, post_likes)

    # Relationships
    relationships = create_sample_relationships(len(users), args.relationships_num)
    submit_relationships(session, relationships)

    # Close the session
    session.close()

    print("Sample data has been added to the database.")
    print(f"Database URL: {args.db_url}")
    print(f"Number of users: {len(users)}")
    print(f"Number of posts: {len(posts)}")
    print(f"Number of comments: {len(comments)}")
    print(f"Number of post likes: {len(post_likes)}")
    print(f"Number of relationships: {len(relationships)}")
