import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from werkzeug.utils import secure_filename

from datetime import date, datetime

from app.forms.registers import RegisterForm
from app.forms.login import LoginForm
from app.forms.edit_account import EditAccountForm
from app.forms.add_movies import AddMoviesForm
from app.models.users import UsersModel
from app.models.movies import MovieModel
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

    if request.method == 'POST':
        dir_image="app/static/img/poster/"

        if request.files:
            image = request.files["image"]
            if image.filename == "":
                print('image must have filename')
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)
            else:
                filename = "poster_%s" % secure_filename(image.filename)

            image.save(os.path.join(dir_image, filename))
            print('image-saved')

        is_onshow = False
        is_upcoming = False
        if request.form['movie_onshow'] == 'yes':
            is_onshow = True

        if request.form['movie_upcoming'] == 'yes':
            is_upcoming = True

        movie = MovieModel(
            movie_title = request.form['movie_title'],
            movie_img_url = f"{dir_image}/{filename}",
            movie_duration = request.form['movie_duration'],
            movie_description = request.form['movie_description'],
            movie_onshow = is_onshow,
            movie_upcoming = is_upcoming,
            movie_released = request.form['movie_released'],
            movie_added = datetime.today()
        )
        
        db.session.add(movie)
        db.session.commit()
        
        return redirect(url_for('auth.index'))
    #return 'Add Movie Page'
    return render_template('admin/add_movies.html', form=form)


@bp.route('/upload', methods=['GET', 'POST'])
#@login_required
def upload():
    dir_image="app/static/img/poster"
    if request.method == "POST":
        if request.files:
            print(request.cookies)
            image = request.files["image"]
            if image.filename == "":
                print('image must have filename')
                return redirect(request.url)
            
            if not allowed_image(image.filename):
                print("That image extension is not allowed")
                return redirect(request.url)
            else:
                filename = "poster_%s" % secure_filename(image.filename)

            image.save(os.path.join(dir_image, filename))

            print('image-saved')
            print(f"{dir_image}/{filename}")
            return redirect(request.url)

    return render_template('upload.html')

def allowed_image(filename):
    if not "." in filename:
        return False
    image_ext_allowed = ["PNG", "JPG", "JPEG", "GIF"]
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in image_ext_allowed:
        return True
    else:
        return False
