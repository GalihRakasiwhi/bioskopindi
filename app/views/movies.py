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
from app.forms.form_movies import MoviesForm
from app.models.model_movie import MovieModel
from app.extensions._db import db
from app.views.functions_plus import allowed_image, clean_tags, m_to_h


bp = Blueprint  ('movie', __name__)

#set dir image
dir_image="static/img/poster/"
dir_image_real="app/static/img/poster/"

@bp.route('/upload', methods=['GET', 'POST'])

@bp.route('/movies', methods=['GET', 'POST'])
def movies():
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    movies = MovieModel.query.all()

    return render_template('admin/movies/movies.html', movies=movies)


@bp.route('/detile/<id>', methods=['GET', 'POST'])
#@login_required
def detile(id):
    form = MoviesForm()
    movies = MovieModel.query.get(id)
    db_date_release = str(movies.movie_released).split()
    db_duration = m_to_h(int(movies.movie_duration))

    return render_template('detile.html', movies=movies, form=form, db_date_release=db_date_release, db_duration=db_duration)
