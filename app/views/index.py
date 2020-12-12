import os
import psycopg2

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from datetime import date, datetime
from app.views.movies import detile
from app.models.model_movie import MovieModel, StudioModel, ScheduleModel
from app.models.model_ticket import TicketModel
from app.models.model_users import UsersModel
from app.models.model_users_admin import UsersAdminModel
from app.extensions._db import db

bp = Blueprint  ('index', __name__)

@bp.route('/')
def index():

    movies = MovieModel.query.all()

    return render_template('index.html', movies=movies)

@bp.route('/test')
def test():
    #set auth
    if not current_user.is_authenticated:
    	flash('Please login!', 'danger')
    	return redirect(url_for('auth.login'))

    return render_template('test.html')