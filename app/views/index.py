import os
import psycopg2

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from datetime import date, datetime
from app.models.users import UsersModel
from app.models.movies import MovieModel
from app.extensions._db import db

bp = Blueprint  ('index', __name__)

@bp.route('/')
def index():
    movies = MovieModel.query.all()
    #return x.username
    return render_template('index.html', movies=movies)
    #return 'Home Page'

@bp.route('/test')
def test():
    return render_template('test.html')