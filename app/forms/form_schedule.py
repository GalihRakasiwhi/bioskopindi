from flask_wtf import FlaskForm
from wtforms import Form, DateField, DecimalField, FloatField, IntegerField, StringField, SubmitField, TimeField, validators
from wtforms.fields.html5 import DateField
from datetime import date, datetime

class ScheduleForm(FlaskForm):
    schedule_movie_id = IntegerField('Movie Name', [ 
        validators.InputRequired(message='Fill the field')
        ])
    schedule_studio_id = IntegerField('Studio Name', [ 
        validators.InputRequired(message='Fill the field')
        ])
    schedule_date = DateField('Schedule Date')
    schedule_time = TimeField('Time', format='%H:%M')
    schedule_price = FloatField('Price', [ 
        validators.InputRequired(message='Fill the field')
        ])
    schedule_schedule_added = DateField('Released', format='%Y-%m-%d', validators=(validators.Optional(),))
    submit_button = SubmitField('Add')
