#from flask_wtf import FlaskForm
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FileField
from wtforms.validators import DataRequired, InputRequired
from flask_wtf.file import FileAllowed

class MovieForm(FlaskForm):
    title = StringField(
        'Movie Title',
        validators=[
            DataRequired(message="Movie title is required")
        ]
    )
    
    description = TextAreaField(
        'Description',
        validators=[
            DataRequired(message="Movie description is required")
        ]
    )
    
    poster = FileField(
        'Movie Poster',
        validators=[
            InputRequired(message="Movie poster is required"),
            FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files (jpg, jpeg, png) are allowed')
        ]
    )