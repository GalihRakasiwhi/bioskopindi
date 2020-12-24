from flask_wtf import FlaskForm, Form
from wtforms import ( #DateField, 
    DateTimeField, FloatField, Form, IntegerField, StringField, PasswordField, SubmitField, 
    TextField, FileField, SelectField, TextAreaField, validators
)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import DateField
from datetime import date, datetime

class BookingTicketorm(FlaskForm):
    bticket_id_user = IntegerField('Id User', [
        validators.InputRequired(message='ID User Required')
        ])
    bticket_id_schedule = IntegerField('Schedule', [
        validators.InputRequired(message='ID Schedule Required')
        ])
    bticket_seats_number = IntegerField('Seats Number', [
        validators.InputRequired(message='Seats Number Required')
        ])
    bticket_price = FloatField('Price', [
        validators.InputRequired(message='Price Required')
        ])
    bticket_status = StringField('Status Payment', [
        validators.InputRequired(message='Status Payment Required')
        ])
    bticket_added = DateTimeField('Booking Ticket Added', default=datetime.today())
    
    submit_button = SubmitField('Buy')