from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256

from app.forms.registers import RegisterForm
from app.forms.login import LoginForm
from app.forms.edit_account import EditAccountForm
from app.forms.add_movies import AddMoviesForm
from app.models.users import UsersModel
from app.extensions._db import db


bp = Blueprint  ('auth', __name__)

@bp.route('/')
def index():
    return render_template('index.html')
    #return 'Home Page'


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
        #return user_object.username
        return redirect(url_for('auth.index'))

    return render_template('auths/login.html', form=form)


@bp.route('/account', methods=['GET', 'POST'])
#@login_required
def account():
    if not current_user.is_authenticated:
    	flash('Please login!', 'danger')
    	return redirect(url_for('auth.login'))

    return render_template('account/account.html')


@bp.route('/edit_account', methods=['GET', 'POST'])
#@login_required
def edit_account():
    form = EditAccountForm()

    if not current_user.is_authenticated:
    	flash('Please login!', 'danger')
    	return redirect(url_for('auth.login'))

    if request.method == 'POST':
        user_object = UsersModel.query.filter_by(username=current_user.username).first()
        user_object.username = request.form['username'],
        user_object.full_name = request.form['full_name'],
        user_object.email = request.form['email']

        db.session.commit()
        return redirect(url_for('auth.index'))
    
    return render_template('account/edit_account.html', form=form)


@bp.route('/logout', methods=['Get'])
def logout():
	logout_user()
	flash('Logout succesfylly', 'success')
	return redirect(url_for('auth.login'))


@bp.route('/add_movies', methods=['GET', 'POST'])
#@login_required
def add_movies():
    form = AddMoviesForm()

    #allow user to login if no validation error
    if form.validate_on_submit():   
        img_dir = os.path.join(
            os.path.dirname(app.instance_path), 'admin/img/poster'
        )

        return redirect(url_for('auth.index'))
    #return 'Add Movie Page'
    return render_template('admin/add_movies.html', form=form)
