import os
import uuid
import bleach
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from flask_wtf import Form
from wtforms.fields.html5 import DateField
from datetime import date, datetime
#from app.forms.form_message_to_system import MesageToSystemForm

from app.extensions._db import db
from app.forms.form_message_payment import MessagePaymentForm
from app.models.model_booking_ticket import BookingTicketModel
from app.models.model_message_to_system import MessageToSystemModel
from app.models.model_payment_status import PaymentStatusModel
from app.models.model_status import StatusModel
from app.models.model_ticket import TicketModel
from app.models.model_users import UsersModel
from app.views.functions_plus import allowed_image, clean_tags, flash_login, flash_login_admin


bp = Blueprint  ('admin_message', __name__)

dir_image="static/img/message/"
dir_image_real="app/static/img/message/"

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

    message = message_list()
    message_status = message_stat()

    message_notification = message_notif()
    return render_template('admin/message/message.html', message=message, 
        message_status=message_status)


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
    message_status = message_stat()
    message_detile = db.session.query(MessageToSystemModel, UsersModel). \
    select_from(MessageToSystemModel).filter_by(id=id). \
    join(UsersModel)
    bticket = BookingTicketModel.query.get(message_detile[0][0].message_bticket_id)
    payment_status = PaymentStatusModel.query.all()

    form = MessagePaymentForm()
    
    message_detile[0][0].message_status = 2 #2 artinya read di tabel status
    db.session.commit()

    if bticket == None:
        flash('Booking Ticket has been deleted by user', 'danger')
        return redirect(url_for('admin_message.message'))

    if request.method == 'POST' and form.validate():
        bticket.bticket_status = request.form['message_payment']
        if payment_status[2].id == int(request.form['message_payment']):
            status = StatusModel.query.get(1)
            seats = bticket.bticket_seats_number.split(',')

            for x in seats:
                unique_ticket_code= str(uuid.uuid4())[:8] 
                create_ticket = TicketModel(
                    ticket_code = unique_ticket_code,
                    ticket_user = bticket.bticket_user_id,
                    ticket_schedule = bticket.bticket_schedule_id,
                    ticket_seat_number = x,
                    ticket_price = bticket.bticket_price/len(seats),
                    ticket_status = status.id,
                    ticket_claimed = False,
                    ticket_added = datetime.today()
                )
                db.session.add(create_ticket)
                db.session.commit()

        flash('Action to Message Payment Successfully', 'success')

        return redirect(url_for('admin_message.message'))
    
    return render_template('admin/message/message_detile.html', bticket=bticket,
        form=form, message=message, message_detile=message_detile, 
        message_status=message_status, payment_status=payment_status)


#Delete Movies ---
@bp.route('/admin/message_delete/<id>', methods=['GET', 'POST'])
#@login_required
def message_delete(id):
    message = MessageToSystemModel.query.get(id)
    
    #user auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    #delete image
    if message.message_img_url != "":  
        message_db_url = message.message_img_url
        filename_in_db = message_db_url.split('/')
        if os.path.exists(f'{dir_image_real}{filename_in_db[-1]}'):
            os.remove(os.path.join(dir_image_real, filename_in_db[-1]))

    #delete movie
    db.session.delete(message)
    db.session.commit()
    print('Message Deleted')

    flash('Delete Message Successfully', 'success')

    return redirect(url_for('admin_message.message'))


def message_list():
    rows_per_page = 10

    #set pagination
    page = request.args.get('page', 1, type=int)

    message = db.session.query(MessageToSystemModel, UsersModel). \
    select_from(MessageToSystemModel).order_by(MessageToSystemModel.message_send_time.desc()). \
    join(UsersModel). \
    paginate(page=page, per_page = rows_per_page)
    
    return message

def message_stat():
    message_status = StatusModel.query.all()
    
    return message_status

def message_notif():

    message = db.session.query(MessageToSystemModel, UsersModel, StatusModel, PaymentStatusModel). \
    select_from(MessageToSystemModel).order_by(MessageToSystemModel.message_send_time.desc()). \
    join(UsersModel).all()
    
    return message