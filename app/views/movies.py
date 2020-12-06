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
from app.views.auths import allowed_image
from app.forms.form_movies import MoviesForm
from app.models.movies import MovieModel
from app.extensions._db import db

bp = Blueprint  ('movie', __name__)

#set dir image
dir_image="static/img/poster/"
dir_image_real="app/static/img/poster/"

@bp.route('/upload', methods=['GET', 'POST'])
#@login_required
def upload():
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

#add Movies ---
@bp.route('/add_movies', methods=['GET', 'POST'])
#@login_required
def add_movies():
    form = MoviesForm()

    #set auth
    if not current_user.is_authenticated:
    	flash('Please login!', 'danger')
    	return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if request.files:
            #req image
            image = request.files["image"]
            if image.filename == "":
                flash('image must have filename', 'danger')
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

        return redirect(url_for('index.index'))
    return render_template('admin/add_movies.html', form=form)


#Edit Movies ---
@bp.route('/edit_movies/<id>', methods=['GET', 'POST'])
#@login_required
def edit_movies(id):
    form = MoviesForm()
    movies = MovieModel.query.get(id)
    #get value onshow
    onshow_data = form.movie_onshow.choices
    is_onshow = movies.movie_onshow
    #get value upcoming
    upcoming_data = form.movie_upcoming.choices
    is_upcoming = movies.movie_upcoming

    db_date_release = str(movies.movie_released).split()

    #user auth
    if not current_user.is_authenticated:
    	flash('Please login!', 'danger')
    	return redirect(url_for('auth.login'))

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
        
        db.session.commit()
        flash('Edit Movie Successfully', 'success')

        return redirect(url_for('index.index'))
    return render_template(
        'admin/edit_movies.html', db_date_release=db_date_release, 
        form=form, is_onshow=is_onshow, is_upcoming=is_upcoming, 
        onshow_data=onshow_data, movies=movies, upcoming_data=upcoming_data
        )

#Delete Movies ---
@bp.route('/delete_movies/<id>', methods=['GET', 'POST'])
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


@bp.route('/detile/<id>', methods=['GET', 'POST'])
#@login_required
def detile(id):
    form = MoviesForm()
    movies = MovieModel.query.get(id)
    db_date_release = str(movies.movie_released).split()
    db_duration = m_to_h(int(movies.movie_duration))

    return render_template('detile.html', movies=movies, form=form, db_date_release=db_date_release, db_duration=db_duration)

#kumpulan Function
def m_to_h(minute):
	if minute <= 60:
		return "%d menit" % minute
	elif minute > 60:
		#print(minute/60)
		x = str(minute/60)
		x = x.split('.')
		#print(x)
		if minute % 60 != 0:
			y = str(minute % 60)
			return f"{x[0]} Jam {y} Menit"
		else:
			return f"{x[0]} Jam"

def clean_tags(text_tag):
    cleaned_tags = bleach.clean(text_tag, 
    tags=[
        'a', 'abbr', 'acronym', 'b', 'br', 'blockquote', 'code', 'em', 
        'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i', 'li', 'ol', 'p',
        'span', 'strong', 'style', 'u','ul'
    ],
    attributes=[{
        'a': ['href', 'title'], 'abbr': ['title'], 'acronym': ['title'],
    },'font', 'style'],
    styles=['background-color', 'color', 'font-family', 'text-align', ],
    protocols=['http', 'https', 'mailto'],
    strip=False, strip_comments=True)

    return cleaned_tags