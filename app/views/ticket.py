import os
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from flask_wtf import Form
from wtforms.fields.html5 import DateField
from app.forms.form_studio import StudioForm
from app.forms.form_ticket import TicketForm
from app.forms.form_movies import MoviesForm
from app.models.model_ticket import TicketModel
from app.models.model_movie import MovieModel, StudioModel, ScheduleModel
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


    ticket = TicketModel.query.all()

    return render_template('ticket/buy_ticket.html')
    #return render_template('admin/ticket/ticket.html', ticket=ticket)

#buy ticket ---
@bp.route('/buy_ticket/<id>', methods=['GET', 'POST'])
#@login_required
def buy_ticket(id):
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    form = TicketForm()

    ticket = TicketModel.query.all()
    schedule = ScheduleModel.query.all()
    movies = MovieModel.query.get(id)

    return render_template(
    	'ticket/buy_ticket.html', 
    	form=form, movies=movies, schedule=schedule
    	)
