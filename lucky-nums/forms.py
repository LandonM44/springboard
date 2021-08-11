from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Email, NumberRange, AnyOf

COLORS = ["red", "green", "orange", "blue"]

class LuckyNumForm(FlaskForm):
    """form for lucky nums"""

    class Meta:
        csrf = False
    
    name = StringField(
        "Name",
        validators=[InputRequired()]
    )
    email = StringField(
        "Email",
        validators=[InputRequired(), Email()]
    )
    year = IntegerField(
        "Year",
        validators=[NumberRange(1900, 2000)]
    )
    color = StringField(
        "Favorite Color",
        validators=[AnyOf(COLORS)]
    )


