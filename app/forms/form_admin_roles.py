from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, validators

class AdminRolesForm(FlaskForm):
    role = StringField('Role Name', [
        validators.Length(min=4, max=128, message='Role name must be between 4 and 128 charachter.'),
        validators.InputRequired(message='Role Name Required')
        ])
    submit_button = SubmitField('Create')
