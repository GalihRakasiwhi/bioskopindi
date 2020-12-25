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
from app.models.model_message_to_system import MessageToSystemModel
from app.models.model_booking_ticket import BookingTicketModel
from app.models.model_users import UsersModel
from app.extensions._db import db
from app.views.functions_plus import allowed_image, clean_tags, flash_login, flash_login_admin, m_to_h


bp = Blueprint  ('admin_message', __name__)


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
    
    return render_template('admin/message/message.html', message=message)

def message_list():
    rows_per_page = 10

    #set pagination
    page = request.args.get('page', 1, type=int)

    message = db.session.query(MessageToSystemModel, UsersModel, BookingTicketModel). \
    select_from(MessageToSystemModel).order_by(MessageToSystemModel.message_send_time.desc()). \
    join(UsersModel). \
    paginate(page=page, per_page = rows_per_page)
    
    return message