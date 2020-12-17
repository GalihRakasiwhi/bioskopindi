import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from werkzeug.utils import secure_filename

from datetime import date, datetime

from app.forms.form_register import RegisterForm
from app.forms.form_login import LoginForm
from app.forms.form_edit_account import EditAccountForm
from app.forms.form_admin_roles import AdminRolesForm
from app.models.model_users import UsersModel
from app.models.model_roles import RolesModel
from app.models.model_users_roles import UsersRolesModel
from app.models.model_message_to_system import MessageToSystemModel
from app.extensions._db import db
from app.views.functions_plus import flash_login, flash_login_admin, allowed_image

bp = Blueprint  ('admin_auth', __name__)


#account
@bp.route('/admin/account', methods=['GET', 'POST'])
#@login_required
def account():
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    #check is admin
    if current_user.user_role[0].role_id != 1:
        flash_login_admin()
        return redirect(url_for('index.index'))

    return render_template('account/account.html')


#Register ---
@bp.route('/admin/register', methods=['GET', 'POST'])
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
        role_object = RolesModel.query.get(1)

        user_role = UsersRolesModel(
            user_id = user_object.id,
            role_id = role_object.id
        )
        db.session.add(user_role)
        db.session.commit()

        return redirect(url_for('admin_auth.login'))

    return render_template('admin/auth/register.html', form=form)


#Login ---
@bp.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    #allow user to login if no validation error
    if form.validate_on_submit():   
        user_object = UsersModel.query.filter_by(username=form.username.data).first()
        login_user(user_object)
        flash('Login succesfylly', 'success')
        return redirect(url_for('index.index'))

    return render_template('auths/login.html', form=form)


#Edit Account---
@bp.route('/admin/edit_account', methods=['GET', 'POST'])
#@login_required
def edit_account():
    form = EditAccountForm()

    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    #check is admin
    if current_user.user_role[0].role_id != 1:
        flash_login_admin()
        return redirect(url_for('index.index'))

    if request.method == 'POST' and form.validate():
        user_object = UsersModel.query.filter_by(username=current_user.username).first()
        user_object.username = request.form['username'],
        user_object.full_name = request.form['full_name'],
        user_object.email = request.form['email']

        db.session.commit()
        return redirect(url_for('admin_auth.account'))
    
    return render_template('account/edit_account.html', form=form)


#User---
@bp.route('/admin/users', methods=['GET', 'POST'])
#@login_required
def users():
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    #check is admin
    if current_user.user_role[0].role_id != 1:
        flash_login_admin()
        return redirect(url_for('index.index'))

    #user_object = UsersModel.query.all()
    user_object = db.session.query(UsersModel, UsersRolesModel, RolesModel). \
    select_from(UsersModel).join(UsersRolesModel).join(RolesModel).all()

    return render_template('admin/auth/users.html', user_object=user_object)



#Roles ---
@bp.route('/admin/roles', methods=['GET', 'POST'])
def roles():
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    #check is admin
    if current_user.user_role[0].role_id != 1:
        flash_login_admin()
        return redirect(url_for('index.index'))

    form = AdminRolesForm()
    roles = RolesModel.query.all()

    return render_template('admin/auth/roles.html', form=form, roles=roles)


#Add Roles
@bp.route('/admin/add_roles', methods=['GET', 'POST'])
def add_roles():
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    form = AdminRolesForm()

    if request.method == "POST" and form.validate():
        roles = RolesModel(
            role = request.form['role']
            )
        db.session.add(roles)
        db.session.commit()

        return redirect(url_for('admin_auth.roles'))

    return render_template('admin/auth/add_roles.html', form=form)

#Add Roles
@bp.route('/admin/edit_roles/<id>', methods=['GET', 'POST'])
def edit_roles(id):
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    form = AdminRolesForm()
    roles = RolesModel.query.get(id)

    if request.method == "POST" and form.validate():
        roles.role = request.form['role']
        db.session.commit()

        return redirect(url_for('admin_auth.roles'))

    return render_template('admin/auth/edit_roles.html', form=form, roles=roles)


#Delete Roles
@bp.route('/admin/delete_roles/<id>', methods=['GET', 'POST'])
def delete_roles(id):
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    form = AdminRolesForm()
    roles = RolesModel.query.get(id)
    db.session.delete(roles)
    db.session.commit()

    return redirect(url_for('admin_auth.roles'))
