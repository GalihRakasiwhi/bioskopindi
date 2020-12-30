import os
import uuid
import bleach
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from flask_wtf import Form
from wtforms.fields.html5 import DateField
from datetime import date, datetime
from app.extensions._db import db

from app.forms.form_movies import MoviesForm
from app.models.model_movie import MovieModel
from app.views.functions_plus import clean_tags, m_to_h, flash_login
from app.views.ticket import message_ticket_list, message_stat

bp = Blueprint  ('movie', __name__)

#set dir image
dir_image="static/img/poster/"
dir_image_real="app/static/img/poster/"

@bp.route('/movies', methods=['GET', 'POST'])
def movies():
    movies = MovieModel.query.all()
    message_ticket = message_ticket_list()
    status = message_stat()
    return render_template('/movies/all_movies.html', message_ticket=message_ticket,
        movies=movies, status=status)


@bp.route('/detile/<id>', methods=['GET', 'POST'])
#@login_required
def detile(id):
    message_ticket = message_ticket_list()
    status = message_stat()
    form = MoviesForm()
    movies = MovieModel.query.get(id)
    db_date_release = str(movies.movie_released).split()
    db_duration = m_to_h(int(movies.movie_duration))

    return render_template('movies/movie_detile.html', db_date_release=db_date_release, 
        db_duration=db_duration, form=form, message_ticket=message_ticket, movies=movies,
        status=status)

@bp.route('/upcoming', methods=['GET', 'POST'])
def upcoming():
    message_ticket = message_ticket_list()
    status = message_stat()
    movies = MovieModel.query.all()

    return render_template('/movies/upcoming.html', message_ticket=message_ticket,
        movies=movies, status=status)
