import os
from flask import (
    Blueprint, current_app, flash, redirect, render_template, request, session, url_for
)
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from flask_wtf import Form
from app.extensions._db import db
from app.models.model_roles import RolesModel


bp = Blueprint  ('test', __name__)

#studio ---
@bp.route('/test', methods=['GET', 'POST'])
#@login_required
def test():
	if not db.session.query(db.exists().where(RolesModel.role == 'Admin')).scalar():
		exists = 'mantul'
	else: exists = 'ok'
	return render_template('test.html', exists=exists)
