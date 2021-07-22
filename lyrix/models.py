from operator import iand
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()

def connect_db(app):
    """connect to database"""
    db.app = app
    db.init_app(app)

class Users(db.Model):
    """Users info"""
    __tablename__ = 'users'

    #primary key for the users id
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #users email stored
    email = db.Column(db.Text, nullable=True)
    #users username stored
    username = db.Column(db.Text, nullable=False, unique=True,)
    #users stored hashed password
    password = db.Column(db.Text, nullable=False)

    #user = db.relationship('Favorite', backref="users")
    user = db.relationship('UserFavorites', backref="users")

    #hashes password and to store in database for the user
    @classmethod
    def signup(cls, username, password, email):
        """Register user with hashed password and return user"""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = Users(
            username=username,
            password=hashed_pwd,
            email=email,
        )
        
        db.session.add(user)
        return user


    #authenticates if a users password is True or False for the users
    @classmethod
    def authentication(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False



class Favorite(db.Model):
    """songs favorited by user"""

    __tablename__ = 'favorites'

    #primary key id 
    id = db.Column(db.Integer, primary_key=True)
    #id of the track
    track_id = db.Column(db.Integer, nullable=False)
    #Foreign key connecting to the Users table and getting the users id 
    artist = db.Column(db.Text, nullable=False)
    #will store id of song 
    title = db.Column(db.Text, nullable=False)
    #artist = db.Column(db.Text, nullable=False)
    #title = db.Column(db.Text, nullable=False)
    
    fav = db.relationship('UserFavorites', backref="favorites")


class UserFavorites(db.Model):
    """maps a playlist to a song"""

    __tablename__ = 'user_favorites'

    #primary key id
    id = db.Column(db.Integer, primary_key=True)
    #id of the user from Users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    #id of the song saved in the Favorite table
    favorite_id = db.Column(db.Integer, db.ForeignKey('favorites.id', ondelete='cascade'))