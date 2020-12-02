from flask_wtf import FlaskForm
from wtforms import (
    DateField, DateTimeField, Form,IntegerField, StringField, PasswordField, SubmitField, 
    TextField, FileField, SelectField, TextAreaField, validators
)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from datetime import date, datetime
from wtforms import (
    Form, StringField, PasswordField, SubmitField, validators, FileField, TextAreaField,
    SelectField, DateField, DateTimeField
)

class AddMoviesForm(FlaskForm):
    movie_title = StringField('Title', [
        validators.Length(min=1, max=64, message='Title must be between 1 and 64 charachter.'), 
        validators.InputRequired(message='Title Required')
        ])
    movie_img_url = FileField('Poster Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
        ])
    movie_duration = IntegerField('Duration', [
        validators.InputRequired(message='Duration Required')
        ])
    movie_description = TextAreaField('Description', [
        validators.InputRequired(message='Description Required')
        ])
    movie_onshow = SelectField(u'is Movie on Show?', choices=[('no'), ('yes')])
    movie_upcoming = SelectField(u'is Movie Upcoming?', choices=[('no'), ('yes')])
    movie_released = DateField('Released (yyyy-mm-dd)', format='%Y-%m-%d', validators=(validators.Optional(),))
    movie_added = DateTimeField('Movie Added', default=datetime.today())

    submit_button = SubmitField('Create')
