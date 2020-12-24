import os
import uuid

from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from flask_wtf import Form
from wtforms.fields.html5 import DateField
from datetime import date, datetime

from app.forms.form_studio import StudioForm
from app.forms.form_ticket import TicketForm
from app.forms.form_movies import MoviesForm
from app.forms.form_booking_ticket import BookingTicketorm
from app.models.model_ticket import TicketModel
from app.models.model_users import UsersModel
from app.models.model_movie import MovieModel, StudioModel, ScheduleModel
from app.models.model_booking_ticket import BookingTicketModel
from app.views.functions_plus import flash_login
from app.extensions._db import db

bp = Blueprint  ('ticket', __name__)

#ticket ---
@bp.route('/ticket/<id>', methods=['GET', 'POST'])
#@login_required
def ticket(id):
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    ticket = TicketModel.query.get(id)
    ticket = db.session.query(TicketModel, ScheduleModel, MovieModel, StudioModel). \
        select_from(TicketModel).filter_by(ticket_user=id). \
        order_by(TicketModel.ticket_added.asc()). \
        join(ScheduleModel). \
        join(MovieModel). \
        join(StudioModel).all()

    return render_template('ticket/ticket.html', ticket=ticket)

#buy ticket ---
@bp.route('/buy_ticket/<id>', methods=['GET', 'POST'])
#@login_required
def buy_ticket(id):
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

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
    
    #schedule[0][1].movie_title

    if request.method == 'POST':
        unique_ticket_code= str(uuid.uuid4())[:8] 
        buy = TicketModel(
            ticket_code = unique_ticket_code,
            ticket_user = current_user.id,
            ticket_schedule = request.form['ticket_schedule'],
            ticket_seat_number = request.form['ticket_seat_number'],
            ticket_payment = 'Waiting for Payment',
            ticket_added = datetime.today()
        )
        
        db.session.add(buy)
        db.session.commit()
        return redirect(url_for('index.index'))

    return render_template(
    	'ticket/buy_ticket.html',
    	form=form, movies=movies, schedule=schedule, schedule_get=schedule_get
    	)


#ticket ---
@bp.route('/booking_ticket/', methods=['GET', 'POST'])
#@login_required
def booking_ticket():
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    booking_ticket = db.session.query(BookingTicketModel, ScheduleModel, MovieModel, StudioModel). \
        select_from(BookingTicketModel).filter_by(bticket_user_id=current_user.id). \
        order_by(BookingTicketModel.bticket_added.asc()). \
        join(ScheduleModel). \
        join(MovieModel). \
        join(StudioModel).all()

    return render_template('ticket/booking_ticket.html', booking_ticket=booking_ticket)


#Select Seat
@bp.route('/select_seat/<id>', methods=['GET', 'POST'])
#@login_required
def select_seat(id):
    form = BookingTicketorm()

    ticket = TicketModel.query.all()
    schedule = ScheduleModel.query.all()
    schedule_get = ScheduleModel.query.get(id)
    movies = MovieModel.query.get(id)

    schedule = db.session.query(ScheduleModel, MovieModel, StudioModel). \
        select_from(ScheduleModel).filter_by(id=id). \
        order_by(ScheduleModel.schedule_date.asc()). \
        join(MovieModel). \
        join(StudioModel).all()


    if request.method == 'POST':
        price = 10000 * len(request.form.getlist('seats'))
        booking = BookingTicketModel(
            bticket_user_id = current_user.id,
            bticket_schedule_id = id,
            bticket_seats_number = request.form.getlist('seats'),
            bticket_price = price,
            bticket_status = 'Waiting for Payment',
            bticket_added = datetime.today()
        )
        
        db.session.add(booking)
        db.session.commit()
        print("schedule id: "+id)
        print(price)
        print(request.form.getlist('seats'))    
        return redirect(url_for('index.index'))

    return render_template(
        'ticket/seat.html', form=form, movies=movies,
        schedule=schedule, schedule_get=schedule_get
        )

