from flask_wtf import FlaskForm, Form
from wtforms import ( #DateField, 
    DateTimeField, Form,IntegerField, StringField, PasswordField, SubmitField, 
    TextField, FileField, SelectField, TextAreaField, validators
)
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.fields.html5 import DateField
from datetime import date, datetime

class MesageToSystemForm(FlaskForm):
    message_user_id = IntegerField('User', [ 
        validators.InputRequired(message='User must define')
        ])
    message_type = SelectField(u'Type Message', choices=[
        ('Confirm Payment'), ('Report Bug'), ('Sugestion')
        ])
    message_text = TextAreaField('Message', [
        validators.InputRequired(message='Message Required')
        ])
    message_img_url = FileField('Image', validators=[
        FileAllowed(['jpg', 'png'], 'Images only!')
        ])
    message_status = SelectField(u'Tpe Message', choices=[
        ('Confirm Payment'), ('Report Bug'), ('Sugestion')
        ])
    message_send_time = DateTimeField('Message Send TIme', default=datetime.today())
    submit_button = SubmitField('Send')
