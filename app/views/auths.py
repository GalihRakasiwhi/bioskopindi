import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from werkzeug.utils import secure_filename

from datetime import date, datetime

from app.extensions._db import db
from app.forms.form_register import RegisterForm
from app.forms.form_login import LoginForm
from app.forms.form_edit_account import EditAccountForm
from app.models.model_users import UsersModel
from app.models.model_roles import RolesModel
from app.models.model_users_roles import UsersRolesModel
from app.models.model_message_to_system import MessageToSystemModel
from app.models.model_booking_ticket import BookingTicketModel
from app.views.functions_plus import allowed_image, flash_login

bp = Blueprint  ('auth', __name__)


#account
@bp.route('/account', methods=['GET', 'POST'])
#@login_required
def account():
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    return render_template('account/account.html')


#Register ---
@bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
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

        user_object = db.session.query(UsersModel).order_by(UsersModel.id.desc()).first()
        role_object = RolesModel.query.get(2)

        user_role = UsersRolesModel(
            user_id = user_object.id,
            role_id = role_object.id
        )
        db.session.add(user_role)
        db.session.commit()
        return redirect(url_for('auth.login'))

    return render_template('auths/register.html', form=form)


#Login ---
@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    #allow user to login if no validation error
    if form.validate_on_submit():   
        user_object = UsersModel.query.filter_by(username=form.username.data).first()
        login_user(user_object)
        flash('Login succesfylly', 'success')
        #return user_object.username
        return redirect(url_for('index.index'))

    return render_template('auths/login.html', form=form)


#Edit Account---
@bp.route('/edit_account', methods=['GET', 'POST'])
#@login_required
def edit_account():
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    form = EditAccountForm()

    if request.method == 'POST':
        user_object = UsersModel.query.filter_by(username=current_user.username).first()
        user_object.username = request.form['username'],
        user_object.full_name = request.form['full_name'],
        user_object.email = request.form['email']

        db.session.commit()
        return redirect(url_for('auth.account'))
    
    return render_template('account/edit_account.html', form=form)


#Logout ---
@bp.route('/logout', methods=['Get'])
def logout():
	logout_user()
	flash('Logout succesfylly', 'success')
	return redirect(url_for('auth.login'))
