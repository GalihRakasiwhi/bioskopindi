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
from app.forms.form_movies import MoviesForm
from app.forms.form_message_to_system import MesageToSystemForm
from app.models.model_message_to_system import MessageToSystemModel
from app.models.model_movie import MovieModel
from app.extensions._db import db
from app.views.functions_plus import allowed_image, clean_tags, m_to_h


bp = Blueprint  ('message', __name__)

#set dir image
dir_image="static/img/message/"
dir_image_real="app/static/img/message/"

@bp.route('/confirm_payment/<id>', methods=['GET', 'POST'])
def confirm_payment(id):
    #set auth
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

    form = MesageToSystemForm()
    if request.method == 'POST':
        if request.files:
            #req image
            image = request.files["image"]
            if image.filename == "":
                flash('must have upload image / image must have filename', 'danger')
                return redirect(request.url)
            
            #chek allowed ext and set filename
            if not allowed_image(image.filename):
                flash('That image extension is not allowed', 'danger')
                return redirect(request.url)
            else:
                ext = image.filename.rsplit(".", 1)[1]
                filename = f"poster_{str(uuid.uuid4())}.{ext}"#secure_filename(image.filename)

        #celaned desc and specify allowed tags
        cleaned_desc = clean_tags(request.form.get('message_text'))
        
        #set to db
        message = MessageToSystemModel(
            message_user_id = current_user.id,
            message_type = request.form['message_type'],
            message_text = f"Confirm Payment for Ticket id: {id}\n " + cleaned_desc,
            message_img_url = f"{dir_image}{filename}",
            message_status = 'Unread',
            message_send_time = datetime.today()
        )
        #save image
        image.save(os.path.join(dir_image_real, filename))
        print('image-saved')

        db.session.add(message)
        db.session.commit()
        flash('Send Confirm Payment Successfully', 'success')

        return redirect(url_for('index.index'))
    return render_template('message/confirm_payment.html', form=form, id=id)

