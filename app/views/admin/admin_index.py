import os
import psycopg2

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from datetime import date, datetime
from app.views.movies import detile
from app.views.functions_plus import flash_login, flash_login_admin
from app.models.model_movie import MovieModel, StudioModel, ScheduleModel
from app.models.model_ticket import TicketModel
from app.models.model_users import UsersModel
from app.models.model_users_admin import UsersAdminModel
from app.models.model_roles import RolesModel
from app.models.model_users_roles import UsersRolesModel
from app.models.model_message_to_system import MessageToSystemModel
from app.views.functions_plus import flash_login, flash_login_admin
from app.views.admin.admin_message import message_list
from app.extensions._db import db

bp = Blueprint  ('admin', __name__)

rows_per_page = 10

@bp.route('/admin/')
def index():

    #check auth
    if not current_user.is_authenticated:
    	flash_login()
    	return redirect(url_for('auth.login'))

    #check is admin
    if current_user.user_role[0].role_id != 1:
        flash_login_admin()
        return redirect(url_for('index.index'))

    movies = MovieModel.query.all()
    studio = StudioModel.query.all()
    schedule = ScheduleModel.query.all()
    ticket = TicketModel.query.all()
    users = UsersModel.query.all()
    #message_unread = MessageToSystemModel.query.all()

    message = message_list()

    return render_template('admin/index.html', 
        movies=movies, message=message, 
        studio=studio, schedule=schedule, 
        ticket=ticket, users=users
        )

    