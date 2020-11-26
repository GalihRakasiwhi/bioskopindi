from wtforms import Form, StringField, PasswordField, SubmitField, validators


class RegisterForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=64)])
    full_name = StringField('Full name', [validators.Length(min=4, max=128)])
    email = StringField('Email', [validators.Length(min=4, max=128)])
    password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('confirm', message='Passwords must match')
    ])
    confirm = PasswordField('Repeat Password')
    submit = SubmitField('Submit')
