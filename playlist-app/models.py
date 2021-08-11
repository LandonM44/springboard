"""Models for Playlist app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

class Playlist(db.Model):
    """Playlist."""
    __tablename__ = 'playlists'
    # ADD THE NECESSARY CODE HERE
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)
    description = db.Column(db.Text)

    songs = db.relationship('Song', secondary="playlist_songs", backref="playlists")
    
class Song(db.Model):
    """Song."""
    __tablename__ = 'songs'
    # ADD THE NECESSARY CODE HERE
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    artist = db.Column(db.Text, nullable=False)

    song = db.relationship('PlaylistSong', backref="songs")


class PlaylistSong(db.Model):
    """Mapping of a playlist to a song."""
    __tablename__ = 'playlist_songs'
    # ADD THE NECESSARY CODE HERE
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    #playlist_id = db.Column(db.Integer, autoincrement=True)
    playlist_id = db.Column(db.Integer, db.ForeignKey('playlists.id'))
    #song_id = db.Column(db.Integer, autoincrement=True)
    song_id = db.Column(db.Integer, db.ForeignKey('songs.id'))



# DO NOT MODIFY THIS FUNCTION
def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
