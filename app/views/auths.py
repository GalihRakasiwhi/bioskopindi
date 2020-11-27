from flask import Blueprint, render_template, request, redirect, url_for
from app.forms.registers import RegisterForm
from app.models.users import UsersModel
from app.extensions._db import db

#from app import db

bp = Blueprint  ('auth', __name__)

@bp.route('/')
def index():
    return 'Home Page'

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        user = UsersModel(
            username = request.form['username'],
            full_name = request.form['full_name'],
            email = request.form['email'],
            password = request.form['password']
            )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('/'))

    return render_template('auths/register.html', form=form)