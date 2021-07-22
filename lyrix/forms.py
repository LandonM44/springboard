from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

#form to login on
class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=3)])


#form for signing up
class SignupForm(FlaskForm):
    """Sign up form"""

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=3)])

#form to search for lyrics of a song
class LyricSearch(FlaskForm):
    """Search for artist in api"""

    artist = StringField('Artist')
    title = StringField('song Title')
    

#form to find song to add to favorites
class AddFavSong(FlaskForm):
    """adds song to favorites"""

    artist = StringField('Artist', validators=[DataRequired()])
    title = StringField('song Title', validators=[DataRequired()])



