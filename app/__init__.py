import os

from flask import Flask
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from app.models.users import UsersModel

def create_app():
    app = Flask(__name__)

    login = LoginManager(app)
    login.init_app(app)
    
    @login.user_loader
    def load_user(id):
        return UsersModel.query.get(int(id))
    
    # config
    app.config.from_object(os.environ['APP_CONFIG_FILE'])

    # extension
    from .extensions._db import db, setup_db
    setup_db(app)

    # view
    from app.views.index import bp as index
    app.register_blueprint(index)

    from app.views.auths import bp as auth
    app.register_blueprint(auth)

    from app.views.movies import bp as movie
    app.register_blueprint(movie)

    return app
