import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app, session
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from werkzeug.utils import secure_filename

from datetime import date, datetime
from app.views.auths import allowed_image
from app.forms.add_movies import AddMoviesForm
from app.models.movies import MovieModel
from app.extensions._db import db

bp = Blueprint  ('movie', __name__)

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

@bp.route('/add_movies', methods=['GET', 'POST'])
#@login_required
def add_movies():
    form = AddMoviesForm()
    if not current_user.is_authenticated:
    	flash('Please login!', 'danger')
    	return redirect(url_for('auth.login'))

    if request.method == 'POST':
        dir_image="static/img/poster/"
        dir_image_real="app/static/img/poster/"
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

            image.save(os.path.join(dir_image_real, filename))
            print('image-saved')

        is_onshow = False
        is_upcoming = False
        if request.form['movie_onshow'] == 'yes':
            is_onshow = True

        if request.form['movie_upcoming'] == 'yes':
            is_upcoming = True

        movie = MovieModel(
            movie_title = request.form['movie_title'],
            movie_img_url = f"{dir_image}{filename}",
            movie_duration = request.form['movie_duration'],
            movie_description = request.form['movie_description'],
            movie_onshow = is_onshow,
            movie_upcoming = is_upcoming,
            movie_released = request.form['movie_released'],
            movie_added = datetime.today()
        )
        
        db.session.add(movie)
        db.session.commit()
        
        return redirect(url_for('index.index'))
    return render_template('admin/add_movies.html', form=form)

@bp.route('/detile/<id>', methods=['GET', 'POST'])
#@login_required
def detile(id):
    form = AddMoviesForm()
    movies = MovieModel.query.get(id)
    duration = m_to_h(int(movies.movie_duration))
    print("mantap mantap mantap")
    print(movies.movie_title)
    return render_template('detile.html', movies=movies, form=form, duration=duration)

def m_to_h(minute):
	if minute <= 60:
		print("%d menit" % minute)
	elif minute > 60:
		print(minute/60)
		x = str(minute/60)
		x = x.split('.')
		print(x)
		if minute % 60 != 0:
			y = str(minute % 60)
			return f"{x[0]} Jam {y} Menit"
		else:
			return f"{x[0]} Jam"
