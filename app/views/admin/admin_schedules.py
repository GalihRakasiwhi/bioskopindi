import os
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from flask_wtf import Form
from wtforms.fields.html5 import DateField
from datetime import date, datetime

from app.extensions._db import db
#from app.forms.form_movies import MoviesForm
from app.forms.form_schedule import ScheduleForm
from app.models.model_movie import MovieModel, StudioModel, ScheduleModel
from app.views.functions_plus import flash_login, flash_login_admin
from app.views.admin.admin_message import message_list, message_stat


bp = Blueprint  ('admin_schedule', __name__)

#schedule ---
@bp.route('/admin/schedule', methods=['GET', 'POST'])
#@login_required
def schedule():
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
    schedule = db.session.query(ScheduleModel, MovieModel, StudioModel). \
    select_from(ScheduleModel).join(MovieModel).join(StudioModel).all()

    return render_template('admin/schedules/schedule.html', message=message, 
        message_status=message_status, schedule=schedule)


#add schedule ---
@bp.route('/admin/add_schedule', methods=['GET', 'POST'])
#@login_required
def add_schedule():
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
    form = ScheduleForm()
    movies = MovieModel.query.all()
    studio = StudioModel.query.all()

    if request.method == 'POST' and form.validate():
        schedule = ScheduleModel(
            schedule_movie_id = request.form['schedule_movie_id'],
            schedule_studio_id = request.form['schedule_studio_id'],
            schedule_date = request.form['schedule_date'],
            schedule_time = request.form['schedule_time'],
            schedule_added = datetime.today()
        )

        db.session.add(schedule)
        db.session.commit()

        return redirect(url_for('admin_schedule.schedule'))

    return render_template('admin/schedules/add_schedule.html', 
        form=form, message=message, message_status=message_status, 
        movies=movies, studio=studio)


#Edit Schedule ---
@bp.route('/admin/edit_schedule/<id>', methods=['GET', 'POST'])
#@login_required
def edit_schedule(id):
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
    form = ScheduleForm()
    movies = MovieModel.query.all()
    studio = StudioModel.query.all()
    schedule = ScheduleModel.query.get(id)

    if request.method == 'POST' and form.validate():
        schedule.schedule_movie_id = request.form['schedule_movie_id'],
        schedule.schedule_studio_id = request.form['schedule_studio_id'],
        schedule.schedule_date = request.form['schedule_date'],
        schedule.schedule_time = request.form['schedule_time'],
    
        db.session.commit()
        flash('Edit Schedule Successfully', 'success')

        return redirect(url_for('admin_schedule.schedule'))

    return render_template('admin/schedules/edit_schedule.html',
        form=form, message=message, message_status=message_status, 
        movies=movies, studio=studio, schedule=schedule)


#Delete Schedule ---
@bp.route('/admin/delete_schedule/<id>', methods=['GET', 'POST'])
#@login_required
def delete_schedule(id):
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    #check is admin
    if current_user.user_role[0].role_id != 1:
        flash_login_admin()
        return redirect(url_for('index.index'))

    schedule = ScheduleModel.query.get(id)
    
    #delete schedule
    db.session.delete(schedule)
    db.session.commit()
    print('schedule Deleted')

    flash('Delete Schedule Successfully', 'success')

    return redirect(url_for('admin_schedule.schedule'))