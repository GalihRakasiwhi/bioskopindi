from flask_wtf import FlaskForm, Form
from wtforms import ( #DateField, 
    DateTimeField, Form,IntegerField, StringField, PasswordField, SubmitField, 
    TextField, FileField, SelectField, TextAreaField, validators
)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import DateField
from datetime import date, datetime

class MoviesForm(FlaskForm):
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
    movie_released = DateField('Released', format='%Y-%m-%d', validators=(validators.Optional(),))
    movie_added = DateTimeField('Movie Added', default=datetime.today())
    
    submit_button = SubmitField('Add')
