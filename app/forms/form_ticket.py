from flask_wtf import FlaskForm
from wtforms import Form, DateField, IntegerField, StringField, SubmitField, TimeField, validators
from wtforms.fields.html5 import DateField
from datetime import date, datetime

class TicketForm(FlaskForm):
    ticket_code = StringField('Ticket Code', [ 
        validators.InputRequired(message='Must Generate Ticket Code')
        ])
    ticket_user = IntegerField('User', [ 
        validators.InputRequired(message='User must define')
        ])
    ticket_schedule = IntegerField('Ticket Schedule')
    ticket_seat_number = IntegerField('Ticket Schedule')
    ticket_payment = StringField('Ticket Payment')
    ticket_status = StringField('Ticket Status')
    ticket_added = DateField('Released', format='%Y-%m-%d')
    submit_button = SubmitField('buy')