from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Email, Length


#form to login on
class LoginForm(FlaskForm):
    """Login form."""

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[Length(min=3)])


#form for signing up
class SignupForm(FlaskForm):
    """Sign up form"""

    email = StringField('E-mail', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=3)])
    profile_img = StringField('(Optional) Image URL')
    

#form for changing or adding to profile
class UserEditForm(FlaskForm):
    """Form for editing users."""

    username = StringField('Username', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired(), Email()])
    image_url = StringField('(Optional) Image URL')
    bio = TextAreaField('(Optional) Tell us about yourself')
    password = PasswordField('Password', validators=[Length(min=6)])


#form to add or edit comments
class CommentForm(FlaskForm):
    """Form to add or edit comments"""

    comment = TextAreaField('text', validators=[DataRequired()])

class NewPost(FlaskForm):
    """form to add a new post"""

    image_url = StringField('add your posts pic', validators=[DataRequired()])
    text = TextAreaField('(optional) add a message with your post')

