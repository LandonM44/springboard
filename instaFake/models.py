from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from datetime import datetime

db = SQLAlchemy()
bcrypt = Bcrypt()


class Follows(db.Model):
    """Connection of a follower <-> followed_user."""

    __tablename__ = 'follows'

    user_being_followed_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True)

    user_following_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="cascade"), primary_key=True)


class Likes(db.Model):
    """Mapping user likes to warbles."""

    __tablename__ = 'likes' 

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id', ondelete='cascade'))


    


class User(db.Model):
    """users info and profile pic"""
    __tablename__ = 'users'

    #primary key for the users id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #users email stored
    email = db.Column(db.Text, nullable=False, unique=True)
    #users username stored
    username = db.Column(db.Text, nullable=False, unique=True,)
    #users stored hashed password
    password = db.Column(db.Text, nullable=False)
    #profile image
    profile_img = db.Column(db.Text, default="/static/images/default-pic.png")
    #profile bio
    bio = db.Column(db.Text)
    #for profile location
    location = db.Column(db.Text)

    post = db.relationship('Posts')

    #followers = db.relationship("follows", backref="users")
    #following = db.relationship("follows", backref="")

    followers = db.relationship("User", secondary="follows", primaryjoin=(Follows.user_being_followed_id == id), secondaryjoin=(Follows.user_following_id == id))

    following = db.relationship("User", secondary="follows", primaryjoin=(Follows.user_following_id == id), secondaryjoin=(Follows.user_being_followed_id == id))

    likes = db.relationship('Posts', secondary="likes")


    @classmethod
    def signup(cls, username, email, password, profile_img):

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            profile_img=profile_img,
        )

        db.session.add(user)
        return user


    @classmethod
    def authenticate(cls, email, password):

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    def is_followed_by(self, other_user):
        """Is this user followed by `other_user`?"""

        found_user_list = [user for user in self.followers if user == other_user]
        return len(found_user_list) == 1

    def is_following(self, other_user):
        """Is this user following `other_use`?"""

        found_user_list = [user for user in self.following if user == other_user]
        return len(found_user_list) == 1


class Posts(db.Model):
    """Comments on posts"""

    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)

    text = db.Column(db.String(140), nullable=False)

    image_url = db.Column(db.Text, nullable=False)

    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)

    user = db.relationship("User")


def connect_db(app):
    """connect to database"""
    db.app = app
    db.init_app(app)

