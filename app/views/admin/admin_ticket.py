import os
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from flask_wtf import Form
from wtforms.fields.html5 import DateField
from app.forms.form_studio import StudioForm
from app.models.model_users import UsersModel
from app.models.model_ticket import TicketModel
from app.models.model_movie import MovieModel, StudioModel, ScheduleModel
from app.views.functions_plus import flash_login, flash_login_admin
from app.views.admin.admin_message import message_list, message_stat
from app.extensions._db import db

bp = Blueprint  ('admin_ticket', __name__)

#ticket ---
@bp.route('/admin/ticket', methods=['GET', 'POST'])
#@login_required
def ticket():
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
    ticket = TicketModel.query.all()
    ticket = db.session.query(TicketModel, UsersModel, ScheduleModel, MovieModel, StudioModel). \
    select_from(TicketModel).join(UsersModel).join(ScheduleModel).join(MovieModel).join(StudioModel).all()
    
    return render_template('admin/ticket/ticket.html', message=message, 
        message_status=message_status, ticket=ticket)
