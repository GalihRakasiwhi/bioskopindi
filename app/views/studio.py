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
from app.extensions._db import db

bp = Blueprint  ('studio', __name__)

#studio ---
@bp.route('/studio', methods=['GET', 'POST'])
#@login_required
def studio():
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    studio = StudioModel.query.all()

    return render_template('admin/studio/studio.html', studio=studio)


#add studio ---
@bp.route('/add_studio', methods=['GET', 'POST'])
#@login_required
def add_studio():

    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))
    
    form = StudioForm()
    
    if request.method == 'POST':

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

    return render_template('admin/studio/add_studio.html', form=form)

#edit studio ---
@bp.route('/edit_studio/<id>', methods=['GET', 'POST'])
#@login_required
def edit_studio(id):
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    form = StudioForm()
    studio = StudioModel.query.get(id)

    if request.method == 'POST':

        #celaned desc and specify allowed tags
        cleaned_desc = clean_tags(request.form.get('studio_description'))
        
        #set rest data to db
        studio.studio_name = request.form['studio_name']
        studio.studio_capacity = request.form['studio_capacity']
        studio.studio_description = cleaned_desc
        
        db.session.commit()
        flash('Edit Studio Successfully', 'success')

        return redirect(url_for('studio.studio'))

    return render_template('admin/studio/edit_studio.html', form=form, studio=studio)
