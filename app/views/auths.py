from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from app.forms.registers import RegisterForm
from app.forms.login import LoginForm
from app.models.users import UsersModel
from app.extensions._db import db

#from app import db

bp = Blueprint  ('auth', __name__)

#login = LoginManager()
#login.init_app(bp)

@bp.route('/')
#@bp.route('/index')
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
        return redirect(url_for('auth.index'))

    return render_template('auths/register.html', form=form)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    #allow user to login if no validation error
    if form.validate_on_submit():
        user_object = UsersModel.query.filter_by(username=form.username.data).first()
        login_user(user_object)
        return redirect(url_for('auth.index'))

    return render_template('auths/login.html', form=form)

@bp.route('/chat', methods=['GET', 'POST'])
@login_required
def chat():
    return 'Chat Room'

@bp.route('/logout', methods=['Get'])
def logout():
	logout_user()
	flash('Logout succesfylly', 'success')
	return redirect(url_for('auth.login'))