from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=3)])



class SignupForm(FlaskForm):
    """Sign up form"""

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=3)])


class LyricSearch(FlaskForm):
    """Search for artist in api"""

    artist = StringField('Artist')
    title = StringField('song Title')

