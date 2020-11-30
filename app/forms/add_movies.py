from flask_wtf import FlaskForm
from wtforms import (
    DateField, Form, StringField, PasswordField, SubmitField, 
    TextField, FileField, SelectField, TextAreaField, validators
)
from flask_wtf.file import FileField, FileAllowed, FileRequired

class AddMoviesForm(FlaskForm):
    movie_title = StringField('Title', [
        validators.Length(min=1, max=64, message='Title must be between 1 and 64 charachter.'), 
        validators.InputRequired(message='Title Required')
        ])
    movie_poster = FileField('Poster Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
        ])
    movie_duration = StringField('Duration', [
        validators.Length(min=4, max=128, message='Name must be between 1 and 128 charachter.'),
        validators.InputRequired(message='Duration Required')
        ])
    movie_description = TextAreaField('Description', [
        validators.InputRequired(message='Description Required')
        ])
    movie_on_show = SelectField(u'is Movie on Show?', choices=[('Yes'), ('No')])
    movie_upcoming = SelectField(u'is Movie Upcoming?', choices=[('Yes'), ('No')])
    movie_released = DateField('Released', format='%m/%d/%Y', validators=(validators.Optional(),))
    movie_added = DateField('Movie Added', format='%m/%d/%Y', validators=(validators.Optional(),))

    submit_button = SubmitField('Create')
