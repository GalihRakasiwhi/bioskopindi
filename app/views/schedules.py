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
from app.forms.form_ticket import TicketForm
from app.models.model_ticket import TicketModel
from app.models.model_movie import MovieModel, StudioModel, ScheduleModel
from app.models.model_ticket import TicketModel
from app.extensions._db import db
from app.views.ticket import message_ticket_list, message_stat

bp = Blueprint  ('schedule', __name__)

#schedule ---
@bp.route('/schedule', methods=['GET', 'POST'])
#@login_required
def schedule():
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    message_ticket = message_ticket_list()
    status = message_stat()
    schedule = db.session.query(ScheduleModel, MovieModel, StudioModel). \
    select_from(ScheduleModel).join(MovieModel).join(StudioModel).all()

    return render_template('schedule/schedule.html', message_ticket=message_ticket,
        schedule=schedule, status=status)


#select schedule
@bp.route('/select_schedule/<id>', methods=['GET', 'POST'])
#@login_required
def select_schedule(id):
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    message_ticket = message_ticket_list()
    status = message_stat()

    form = TicketForm()

    ticket = TicketModel.query.all()
    schedule = ScheduleModel.query.all()
    schedule_get = ScheduleModel.query.get(id)
    movies = MovieModel.query.get(id)

    schedule = db.session.query(ScheduleModel, MovieModel, StudioModel). \
        select_from(ScheduleModel). \
        order_by(ScheduleModel.schedule_date.asc()). \
        join(MovieModel).filter_by(id=id). \
        join(StudioModel).all()

    if request.method == 'POST':
        #unique_ticket_code= str(uuid.uuid4())[:8] 
#        buy = TicketModel(
#            #ticket_code = unique_ticket_code,
#            ticket_user = current_user.id,
#            ticket_schedule = request.form['ticket_schedule'],
#            ticket_seat_number = request.form['ticket_seat_number'],
#            ticket_payment = 'Waiting for Payment',
#            ticket_added = datetime.today()
#        )
        
#        db.session.add(buy)
#        db.session.commit()
        return redirect(url_for('ticket.select_seat', id=request.form['ticket_schedule']))

    return render_template(
        'schedule/select_schedule.html',
        form=form, message_ticket=message_ticket, movies=movies, 
        schedule=schedule, schedule_get=schedule_get, status=status)

