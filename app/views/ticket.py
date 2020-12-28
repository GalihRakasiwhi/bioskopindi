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
from app.models.model_payment_status import PaymentStatusModel
from app.models.model_status import StatusModel
from app.models.model_ticket import TicketModel
from app.models.model_users import UsersModel
from app.models.model_movie import MovieModel, StudioModel, ScheduleModel
from app.models.model_booking_ticket import BookingTicketModel
from app.views.functions_plus import flash_login
from app.extensions._db import db

bp = Blueprint  ('ticket', __name__)

#ticket ---
@bp.route('/ticket/', methods=['GET', 'POST'])
#@login_required
def ticket():
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    message_ticket = message_ticket_list()
    status = message_stat()

    ticket = db.session.query(TicketModel, ScheduleModel, MovieModel, StudioModel, StatusModel). \
        select_from(TicketModel).filter_by(ticket_user=current_user.id). \
        order_by(TicketModel.ticket_added.asc()). \
        join(ScheduleModel). \
        join(MovieModel). \
        join(StudioModel). \
        join(StatusModel).all()

    return render_template('ticket/ticket.html', message_ticket=message_ticket,
        status=status, ticket=ticket)


#ticket ---
@bp.route('/booking_ticket/', methods=['GET', 'POST'])
#@login_required
def booking_ticket():
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    message_ticket = message_ticket_list()
    status = message_stat()

    booking_ticket = db.session.query(BookingTicketModel, ScheduleModel, MovieModel, StudioModel, PaymentStatusModel). \
        select_from(BookingTicketModel).filter_by(bticket_user_id=current_user.id). \
        order_by(BookingTicketModel.bticket_added.asc()). \
        join(ScheduleModel). \
        join(MovieModel). \
        join(StudioModel). \
        join(PaymentStatusModel).all()

    return render_template('ticket/booking_ticket.html', booking_ticket=booking_ticket,
        message_ticket=message_ticket, status=status)


#Select Seat
@bp.route('/select_seat/<id>', methods=['GET', 'POST'])
#@login_required
def select_seat(id):
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    message_ticket = message_ticket_list()
    status = message_stat()

    form = BookingTicketorm()

    ticket = TicketModel.query.all()
    schedule = ScheduleModel.query.all()
    schedule_get = ScheduleModel.query.get(id)
    movies = MovieModel.query.get(id)
    payment_status = PaymentStatusModel.query.get(1)

    schedule = db.session.query(ScheduleModel, MovieModel, StudioModel). \
        select_from(ScheduleModel).filter_by(id=id). \
        order_by(ScheduleModel.schedule_date.asc()). \
        join(MovieModel). \
        join(StudioModel).all()

    if request.method == 'POST':
        price = 10000 * len(request.form.getlist('seats'))

        ticket_get = str(request.form.getlist('seats')). \
        replace("{", "").replace("}", ""). \
        replace("[", "").replace("]", ""). \
        replace("'", "").replace(" ", "")

        booking = BookingTicketModel(
            bticket_user_id = current_user.id,
            bticket_schedule_id = id,
            bticket_seats_number = ticket_get,
            bticket_price = price,
            bticket_status = payment_status.id,
            bticket_added = datetime.today()
        )
        
        db.session.add(booking)
        db.session.commit()
        return redirect(url_for('index.index'))

    return render_template(
        'ticket/seat.html', form=form, message_ticket=message_ticket, movies=movies,
        schedule=schedule, schedule_get=schedule_get, status=status
        )


#Ticket Detile
@bp.route('/ticket_detile/<id>', methods=['GET', 'POST'])
#@login_required
def ticket_detile(id):
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    message_ticket = message_ticket_list()
    status = message_stat()

    ticket = db.session.query(TicketModel, ScheduleModel, MovieModel, StudioModel). \
        select_from(TicketModel).filter_by(id=id). \
        join(ScheduleModel). \
        join(MovieModel). \
        join(StudioModel).first()

    ticket[0].ticket_status = 2
    db.session.commit()

    return render_template('ticket/ticket_detile.html', message_ticket=message_ticket,
        status=status, ticket=ticket)


def message_ticket_list():
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    message_ticket = db.session.query(TicketModel, ScheduleModel, UsersModel, MovieModel). \
    select_from(TicketModel).order_by(TicketModel.ticket_added.desc()). \
    join(ScheduleModel).join(UsersModel).join(MovieModel).all()

    return message_ticket

def message_stat():
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    status = StatusModel.query.all()

    return status
