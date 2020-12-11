import os
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from flask_wtf import Form
from wtforms.fields.html5 import DateField
from datetime import date, datetime
from app.views.movies import detile
from app.forms.form_movies import MoviesForm
from app.forms.form_schedule import ScheduleForm
from app.models.model_movie import MovieModel, StudioModel, ScheduleModel
from app.models.model_ticket import TicketModel
from app.extensions._db import db

bp = Blueprint  ('schedule', __name__)

#schedule ---
@bp.route('/schedule', methods=['GET', 'POST'])
#@login_required
def schedule():
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    #movies = MovieModel.query.all()
    #schedule = ScheduleModel.query.all()
    schedule = db.session.query(ScheduleModel, MovieModel, StudioModel). \
    select_from(ScheduleModel).join(MovieModel).join(StudioModel).all()

    #movies = MovieModel.query.filter_by(id=1).first()
    #print(movies.movie_schedule)

    return render_template('admin/schedules/schedule.html', schedule=schedule)


#add schedule ---
@bp.route('/add_schedule', methods=['GET', 'POST'])
#@login_required
def add_schedule():
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    form = ScheduleForm()
    movies = MovieModel.query.all()
    studio = StudioModel.query.all()

    if request.method == 'POST':

        schedule = ScheduleModel(
            schedule_movie_id = request.form['schedule_movie_id'],
            schedule_studio_id = request.form['schedule_studio_id'],
            schedule_start_date = request.form['schedule_start_date'],
            schedule_end_date = request.form['schedule_end_date'],
            schedule_time = request.form['schedule_time'],
            schedule_added = datetime.today()
        )

        db.session.add(schedule)
        db.session.commit()

        return redirect(url_for('schedule.schedule'))

    return render_template('admin/schedules/add_schedule.html', form=form, movies=movies, studio=studio)


#Edit Schedule ---
@bp.route('/edit_schedule/<id>', methods=['GET', 'POST'])
#@login_required
def edit_schedule(id):
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    form = ScheduleForm()
    movies = MovieModel.query.all()
    studio = StudioModel.query.all()
    schedule = ScheduleModel.query.get(id)

    if request.method == 'POST':
        schedule.schedule_movie_id = request.form['schedule_movie_id'],
        schedule.schedule_studio_id = request.form['schedule_studio_id'],
        schedule.schedule_start_date = request.form['schedule_start_date'],
        schedule.schedule_end_date = request.form['schedule_end_date'],
        schedule.schedule_time = request.form['schedule_time'],
    
        db.session.commit()
        flash('Edit Schedule Successfully', 'success')

        return redirect(url_for('schedule.schedule'))

    return render_template('admin/schedules/edit_schedule.html',
        form=form, movies=movies, studio=studio, schedule=schedule
        )


#Delete Schedule ---
@bp.route('/delete_schedule/<id>', methods=['GET', 'POST'])
#@login_required
def delete_schedule(id):
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    schedule = ScheduleModel.query.get(id)
    
    #delete schedule
    db.session.delete(schedule)
    db.session.commit()
    print('schedule Deleted')

    flash('Delete Schedule Successfully', 'success')

    return redirect(url_for('schedule.schedule'))