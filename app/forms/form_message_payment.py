from flask_wtf import FlaskForm, Form
from wtforms import Form,IntegerField, StringField, SubmitField, SelectField, validators

class MessagePaymentForm(FlaskForm):
    message_payment = SelectField(u'Action', choices=[('Payment Confirmed'), ('Payment Declined')])
    submit_button = SubmitField('Submit')
