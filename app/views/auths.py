from flask import Blueprint, render_template, request
from app.forms.registers import RegisterForm

bp = Blueprint('auth', __name__)

@bp.route('/')
def index():
    return 'Home Page'

@bp.route('/register', methods=('GET', 'POST'))
def register():
    form = RegisterForm()

    if request.method == 'POST':
        username = request.form['username']
        full_name = request.form['full_name']
        email = request.form['email']
        password = request.form['password']
        role_id = 'user'
        db = get_db()
        error = None

    return render_template('auths/register.html', form=form)