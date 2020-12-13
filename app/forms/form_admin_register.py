from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, validators

class AdminRegisterForm(FlaskForm):
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
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.InputRequired(message='Password Required'),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm_password = PasswordField('Repeat Password', [
        validators.InputRequired(message='Confirm Password')
    ])
    submit_button = SubmitField('Create')
