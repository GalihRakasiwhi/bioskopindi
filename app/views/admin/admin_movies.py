import os
import uuid
import bleach
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from werkzeug.utils import secure_filename
from flask_wtf import Form
from wtforms.fields.html5 import DateField
from datetime import date, datetime

from app.extensions._db import db
from app.forms.form_movies import MoviesForm
from app.models.model_movie import MovieModel
from app.views.functions_plus import allowed_image, clean_tags, flash_login, flash_login_admin, m_to_h
from app.views.admin.admin_message import message_list, message_stat

bp = Blueprint  ('admin_movies', __name__)

#set dir image
dir_image="static/img/poster/"
dir_image_real="app/static/img/poster/"
rows_per_page = 10

@bp.route('/admin/movies', methods=['GET', 'POST'])
def movies():
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    #check is admin
    if current_user.user_role[0].role_id != 1:
        flash_login_admin()
        return redirect(url_for('index.index'))

    message = message_list()
    message_status = message_stat()
    #set pagination
    page = request.args.get('page', 1, type=int)

    movies = MovieModel.query.order_by(MovieModel.movie_added.desc()). \
    paginate(page=page, per_page = rows_per_page)

    #movies = MovieModel.query.all()

    return render_template('admin/movies/movies.html', movies=movies, message=message, 
        message_status=message_status)

#add Movies ---
@bp.route('/admin/add_movies', methods=['GET', 'POST'])
#@login_required
def add_movies():
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    #check is admin
    if current_user.user_role[0].role_id != 1:
        flash_login_admin()
        return redirect(url_for('index.index'))

    message = message_list()
    message_status = message_stat()
    form = MoviesForm()

    if request.method == 'POST':
        if request.files:
            #req image
            image = request.files["image"]
            if image.filename == "":
                flash('must have upload image / image must have filename', 'danger')
                return redirect(request.url)
            
            #chek allowed ext and set filename
            if not allowed_image(image.filename):
                flash('That image extension is not allowed', 'danger')
                return redirect(request.url)
            else:
                ext = image.filename.rsplit(".", 1)[1]
                filename = f"poster_{str(uuid.uuid4())}.{ext}"#secure_filename(image.filename)

            #save image
            image.save(os.path.join(dir_image_real, filename))
            print('image-saved')

        #define onshow and upcoming value
        is_onshow = False
        is_upcoming = False
        if request.form['movie_onshow'] == 'yes':
            is_onshow = True
        if request.form['movie_upcoming'] == 'yes':
            is_upcoming = True

        #celaned desc and specify allowed tags
        cleaned_desc = clean_tags(request.form.get('movie_description'))
        
        #set to db
        movie = MovieModel(
            movie_title = request.form['movie_title'],
            movie_img_url = f"{dir_image}{filename}",
            movie_duration = request.form['movie_duration'],
            movie_description = cleaned_desc,
            movie_onshow = is_onshow,
            movie_upcoming = is_upcoming,
            movie_released = request.form['movie_released'],
            movie_added = datetime.today()
        )
        
        db.session.add(movie)
        db.session.commit()
        flash('Adding Movie Successfully', 'success')

        return redirect(url_for('admin_movies.movies'))
    return render_template('admin/movies/add_movies.html', form=form, message=message,
        message_status=message_status)


#Edit Movies ---
@bp.route('/admin/edit_movies/<id>', methods=['GET', 'POST'])
#@login_required
def edit_movies(id):
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    #check is admin
    if current_user.user_role[0].role_id != 1:
        flash_login_admin()
        return redirect(url_for('index.index'))
    
    message = message_list()
    message_status = message_stat()
    form = MoviesForm()
    movies = MovieModel.query.get(id)
    #get value onshow
    onshow_data = form.movie_onshow.choices
    is_onshow = movies.movie_onshow
    #get value upcoming
    upcoming_data = form.movie_upcoming.choices
    is_upcoming = movies.movie_upcoming

    db_date_release = str(movies.movie_released).split()

    if request.method == 'POST':
        if request.files:
            image = request.files["image"]
            if image.filename == "":
                movies.movie_img_url == movies.movie_img_url
            else:
                if not allowed_image(image.filename):
                    flash("That image extension is not allowed")
                    return redirect(request.url)

                ext = image.filename.rsplit(".", 1)[1]
                filename = f"poster_{str(uuid.uuid4())}.{ext}"
                #delete image
                poster_db_url = movies.movie_img_url
                filename_in_db = poster_db_url.split('/')
                os.remove(os.path.join(dir_image_real, filename_in_db[-1]))

                #save image
                image.save(os.path.join(dir_image_real, filename))
                movies.movie_img_url = f"{dir_image}{filename}",
                print('image-saved')

        #set movie onshow
        if request.form['movie_onshow'] == 'yes':
            movies.movie_onshow = True
        else :
            movies.movie_onshow = False

        #set movie upcoming
        if request.form['movie_upcoming'] == 'yes':
            movies.movie_upcoming = True
        else :
            movies.movie_upcoming = False
        
        #celaned desc and specify allowed tags
        cleaned_desc = clean_tags(request.form.get('movie_description'))

        #set rest data to db
        movies.movie_title = request.form['movie_title']
        #movies.movie_img_url = f"{dir_image}{filename}",
        movies.movie_duration = request.form['movie_duration']
        movies.movie_description = cleaned_desc
        movies.movie_released = request.form['movie_released']
        movies.movie_edited = datetime.today()

        db.session.commit()
        flash('Edit Movie Successfully', 'success')

        return redirect(url_for('index.index'))
    return render_template(
        'admin/movies/edit_movies.html', db_date_release=db_date_release, 
        form=form, is_onshow=is_onshow, is_upcoming=is_upcoming, 
        onshow_data=onshow_data, message=message, message_status=message_status, 
        movies=movies, upcoming_data=upcoming_data)

#Delete Movies ---
@bp.route('/admin/delete_movies/<id>', methods=['GET', 'POST'])
#@login_required
def delete_movies(id):
    movies = MovieModel.query.get(id)
    
    #user auth
    if not current_user.is_authenticated:
    	flash('Please login!', 'danger')
    	return redirect(url_for('auth.login'))

    #delete image
    if movies.movie_img_url != "":
        poster_db_url = movies.movie_img_url
        filename_in_db = poster_db_url.split('/')
        if os.path.exists(f'{dir_image_real}{filename_in_db[-1]}'):
            os.remove(os.path.join(dir_image_real, filename_in_db[-1]))

    #delete movie
    db.session.delete(movies)
    db.session.commit()
    print('Movie Deleted')

    flash('Delete Movie Successfully', 'success')

    return redirect(url_for('index.index'))


@bp.route('/admin/detile/<id>', methods=['GET', 'POST'])
#@login_required
def detile(id):
    message = message_list()
    message_status = message_stat()
    form = MoviesForm()
    movies = MovieModel.query.get(id)
    db_date_release = str(movies.movie_released).split()
    db_duration = m_to_h(int(movies.movie_duration))

    return render_template('/admin/movies/detile.html', 
        message=message, message_status=message_status, movies=movies, form=form, 
        db_date_release=db_date_release, db_duration=db_duration
        )
