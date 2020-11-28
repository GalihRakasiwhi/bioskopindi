from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, validators, ValidationError
from app.models.users import UsersModel
from passlib.hash import pbkdf2_sha256

def invalid_credentials(form, field):
    #username and password checker
    username_entered = form.username.data
    password_entered = field.data

    #check username is valid
    user_object = UsersModel.query.filter_by(username=username_entered).first()
    
    if user_object is None: #jika username tidak ada
        raise ValidationError('Username or Password is incorect.')
    elif not pbkdf2_sha256.verify(password_entered, user_object.password):
        raise ValidationError('Username or Password is incorect.')


class LoginForm(FlaskForm):
    username = StringField('Username', [validators.InputRequired(message='Username Required')])
    password = PasswordField('Password', [
        validators.InputRequired(message='Password Required'),
        invalid_credentials
        ])
    submit_button = SubmitField('Login')
