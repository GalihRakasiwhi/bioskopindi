from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256

from app.forms.registers import RegisterForm
from app.forms.login import LoginForm
from app.models.users import UsersModel
from app.extensions._db import db


bp = Blueprint  ('auth', __name__)

@bp.route('/')
def index():
    return 'Home Page'

@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST':
        password = form.password.data
        #hash Password
        hashed_password = pbkdf2_sha256.hash(password)

        user = UsersModel(
            username = request.form['username'],
            full_name = request.form['full_name'],
            email = request.form['email'],
            password = hashed_password #request.form['password']
        )
        
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('auth.login'))

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
#@login_required
def chat():
    if not current_user.is_authenticated:
    	flash('Please login!', 'danger')
    	return redirect(url_for('auth.login'))
    return 'Chat Room'

@bp.route('/logout', methods=['Get'])
def logout():
	logout_user()
	flash('Logout succesfylly', 'success')
	return redirect(url_for('auth.login'))