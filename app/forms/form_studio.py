from flask_wtf import FlaskForm
from wtforms import Form, DateField, IntegerField, StringField, SubmitField, TextAreaField, validators

class StudioForm(FlaskForm):
    studio_name = StringField('Studio Name', [ 
        validators.InputRequired(message='Fill the field')
        ])
    studio_capacity = IntegerField('Studio Capacity', [ 
        validators.InputRequired(message='Fill the field')
        ])
    studio_description = TextAreaField('Description', [
        validators.InputRequired(message='Description Required')
        ])
    submit_button = SubmitField('Add')
