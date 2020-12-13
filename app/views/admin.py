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
from app.models.model_roles import RolesModel
from app.models.model_users_roles import UsersRolesModel
from app.models.model_message_to_system import MessageToSystemModel

from app.extensions._db import db

bp = Blueprint  ('admin', __name__)

@bp.route('/admin/')
def index():

    #set auth
    if not current_user.is_authenticated:
    	flash('Please login!', 'danger')
    	return redirect(url_for('auth.login'))

    movies = MovieModel.query.all()
    studio = StudioModel.query.all()
    schedule = ScheduleModel.query.all()
    ticket = TicketModel.query.all()
    users = UsersModel.query.all()

    return render_template('admin/index.html', movies=movies, studio=studio, schedule=schedule, ticket=ticket, users=users)

@bp.route('/test')
def test():
    return render_template('test.html')