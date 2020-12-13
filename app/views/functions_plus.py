import os
import uuid
import bleach

from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from werkzeug.utils import secure_filename

from datetime import date, datetime

#kumpulan Function

def allowed_image(filename):
    if not "." in filename:
        return False
    image_ext_allowed = ["PNG", "JPG", "JPEG", "GIF"]
    ext = filename.rsplit(".", 1)[1]
    if ext.upper() in image_ext_allowed:
        return True
    else:
        return False

#set auth
def check_login():
    if not current_user.is_authenticated:
        flash('Please login!', 'danger')
        return redirect(url_for('auth.login'))

#convert minute to hour
def m_to_h(minute):
	if minute <= 60:
		return "%d menit" % minute
	elif minute > 60:
		#print(minute/60)
		x = str(minute/60)
		x = x.split('.')
		#print(x)
		if minute % 60 != 0:
			y = str(minute % 60)
			return f"{x[0]} Jam {y} Menit"
		else:
			return f"{x[0]} Jam"

#clean Tags
def clean_tags(text_tag):
    cleaned_tags = bleach.clean(text_tag, 
    tags=[
        'a', 'abbr', 'acronym', 'b', 'br', 'blockquote', 'code', 'em', 
        'font', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'i', 'li', 'ol', 'p',
        'span', 'strong', 'style', 'u','ul'
    ],
    attributes=[{
        'a': ['href', 'title'], 'abbr': ['title'], 'acronym': ['title'],
    },'font', 'style'],
    styles=['background-color', 'color', 'font-family', 'text-align', ],
    protocols=['http', 'https', 'mailto'],
    strip=False, strip_comments=True)

    return cleaned_tags