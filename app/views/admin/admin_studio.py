import os
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from flask_wtf import Form
from wtforms.fields.html5 import DateField
from app.forms.form_studio import StudioForm
from app.models.model_movie import MovieModel, StudioModel
from app.views.movies import clean_tags
from app.views.functions_plus import flash_login, flash_login_admin
from app.views.admin.admin_message import message_list, message_stat
from app.extensions._db import db

bp = Blueprint  ('admin_studio', __name__)

#studio ---
@bp.route('/admin/studio', methods=['GET', 'POST'])
#@login_required
def studio():
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
    studio = StudioModel.query.all()

    return render_template('admin/studio/studio.html', message=message,
        message_status=message_status, studio=studio)


#add studio ---
@bp.route('/admin/add_studio', methods=['GET', 'POST'])
#@login_required
def add_studio():
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
    form = StudioForm()
    
    if request.method == 'POST' and form.validate():

        #celaned desc and specify allowed tags
        cleaned_desc = clean_tags(request.form.get('studio_description'))
        
        #set to db
        studio = StudioModel(
            studio_name = request.form['studio_name'],
            studio_capacity = request.form['studio_capacity'],
            studio_description = cleaned_desc
        )
        
        db.session.add(studio)
        db.session.commit()
        flash('Adding Studio Successfully', 'success')

        return redirect(url_for('studio.studio'))

    return render_template('admin/studio/add_studio.html', form=form, message=message,
        message_status=message_status)

#edit studio ---
@bp.route('/admin/edit_studio/<id>', methods=['GET', 'POST'])
#@login_required
def edit_studio(id):
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
    form = StudioForm()
    studio = StudioModel.query.get(id)

    if request.method == 'POST' and form.validate():

        #celaned desc and specify allowed tags
        cleaned_desc = clean_tags(request.form.get('studio_description'))
        
        #set rest data to db
        studio.studio_name = request.form['studio_name']
        studio.studio_capacity = request.form['studio_capacity']
        studio.studio_description = cleaned_desc
        
        db.session.commit()
        flash('Edit Studio Successfully', 'success')

        return redirect(url_for('studio.studio'))

    return render_template('admin/studio/edit_studio.html', 
        form=form, message=message, message_status=message_status, studio=studio)
