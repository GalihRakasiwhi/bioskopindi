import os
import uuid
import bleach
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from passlib.hash import pbkdf2_sha256
from werkzeug.utils import secure_filename

from flask_wtf import Form
from wtforms.fields.html5 import DateField
from datetime import date, datetime
from app.forms.form_message_to_system import MesageToSystemForm
from app.forms.form_message_payment import MessagePaymentForm
from app.models.model_message_to_system import MessageToSystemModel
from app.models.model_booking_ticket import BookingTicketModel
from app.models.model_ticket import TicketModel
from app.models.model_users import UsersModel
from app.extensions._db import db
from app.views.functions_plus import allowed_image, clean_tags, flash_login, flash_login_admin, m_to_h


bp = Blueprint  ('admin_message', __name__)

#admin message
@bp.route('/admin/message/', methods=['GET', 'POST'])
def message():
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    #check is admin
    if current_user.user_role[0].role_id != 1:
        flash_login_admin()
        return redirect(url_for('index.index'))

    #set pagination
    page = request.args.get('page', 1, type=int)

    #message = MessageToSystemModel.query.order_by(MessageToSystemModel.message_send_time.desc()). \
    #paginate(page=page, per_page = rows_per_page). \

    #message = db.session.query(MessageToSystemModel, UsersModel). \
    #select_from(MessageToSystemModel).order_by(MessageToSystemModel.message_send_time.desc()). \
    #join(UsersModel). \
    #paginate(page=page, per_page = rows_per_page)
    
    #join(UsersModel).all()
    message = message_list()
    message_notification = message_notif()
    return render_template('admin/message/message.html', message=message, 
        message_notification=message_notification)


#message detile
@bp.route('/admin/message_detile/<id>', methods=['GET', 'POST'])
def message_detile(id):
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    #check is admin
    if current_user.user_role[0].role_id != 1:
        flash_login_admin()
        return redirect(url_for('index.index'))

    #set pagination
    message = message_list()

    form = MessagePaymentForm()

    message_detile = db.session.query(MessageToSystemModel, UsersModel, BookingTicketModel). \
    select_from(MessageToSystemModel).filter_by(id=id). \
    join(UsersModel).join(BookingTicketModel)

    
    message_detile[0][0].message_status = 'Read'
    db.session.commit()

    if request.method == 'POST' and form.validate():
        message_detile[0][2].bticket_status = request.form['message_payment']
        
        ticket = TicketModel.query.all()    
        unique_ticket_code= str(uuid.uuid4())[:8] 
        create_ticket = TicketModel(
            ticket_code = unique_ticket_code,
            ticket_user = current_user.id,
            ticket_schedule = request.form['ticket_schedule'],
            ticket_seat_number = request.form['ticket_seat_number'],
            ticket_payment = 'Waiting for Payment',
            ticket_added = datetime.today()
        )
        
        db.session.add(create_ticket)
        db.session.commit()
        flash('Action to Message Payment Successfully', 'success')

        return redirect(url_for('admin_message.message'))

    return render_template('admin/message/message_detile.html', form=form,
        message=message, message_detile=message_detile)



def message_list():
    rows_per_page = 10

    #set pagination
    page = request.args.get('page', 1, type=int)

    message = db.session.query(MessageToSystemModel, UsersModel). \
    select_from(MessageToSystemModel).order_by(MessageToSystemModel.message_send_time.desc()). \
    join(UsersModel). \
    paginate(page=page, per_page = rows_per_page)
    
    return message

def message_notif():

    message = db.session.query(MessageToSystemModel, UsersModel). \
    select_from(MessageToSystemModel).order_by(MessageToSystemModel.message_send_time.desc()). \
    join(UsersModel).all()
    
    return message