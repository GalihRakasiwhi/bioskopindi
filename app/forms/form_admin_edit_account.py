from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, validators

class AdminEditAccountForm(FlaskForm):
    username = StringField('Username', [
        validators.Length(min=4, max=25, message='Username must be between 4 and 25 charachter.'), 
        validators.InputRequired(message='Username Required')
        ])
    full_name = StringField('Full name', [
        validators.Length(min=4, max=128, message='Name must be between 4 and 128 charachter.'),
        validators.InputRequired(message='Full Name Required')
        ])
    email = StringField('Email', [
        validators.Length(min=4, max=128),
        validators.InputRequired(message='Email Required')
        ])
    submit_button = SubmitField('Edit')
