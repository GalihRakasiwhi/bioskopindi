import os
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from flask_wtf import Form
from wtforms.fields.html5 import DateField

from app.extensions._db import db
from app.models.model_movie import MovieModel, StudioModel
from app.views.movies import clean_tags
from app.views.ticket import message_ticket_list, message_stat
from app.views.functions_plus import flash_login

bp = Blueprint  ('studio', __name__)

#studio ---
@bp.route('/studio', methods=['GET', 'POST'])
#@login_required
def studio():
    #check auth
    if not current_user.is_authenticated:
        flash_login()
        return redirect(url_for('auth.login'))

    message_ticket = message_ticket_list()
    status = message_stat()
    studio = StudioModel.query.all()

    return render_template('/', message_ticket=message_ticket,
        status=status, studio=studio)

