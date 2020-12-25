import os

from flask import Flask
from flask_login import LoginManager, login_user, current_user, login_required, logout_user

from app.models.model_users import UsersModel

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

    # ---- view admin
    from app.views.admin.admin_index import bp as admin
    app.register_blueprint(admin)

    from app.views.admin.admin_auth import bp as admin_auth
    app.register_blueprint(admin_auth)

    from app.views.admin.admin_movies import bp as admin_movies
    app.register_blueprint(admin_movies)

    from app.views.admin.admin_schedules import bp as admin_schedules
    app.register_blueprint(admin_schedules)

    from app.views.admin.admin_studio import bp as admin_studio
    app.register_blueprint(admin_studio)

    from app.views.admin.admin_ticket import bp as admin_ticket
    app.register_blueprint(admin_ticket)

    from app.views.admin.admin_message import bp as admin_message
    app.register_blueprint(admin_message)



    # ---- view user
    from app.views.index import bp as index
    app.register_blueprint(index)

    from app.views.auths import bp as auth
    app.register_blueprint(auth)

    from app.views.movies import bp as movie
    app.register_blueprint(movie)

    from app.views.schedules import bp as schedule
    app.register_blueprint(schedule)

    from app.views.studio import bp as studio
    app.register_blueprint(studio)

    from app.views.ticket import bp as ticket
    app.register_blueprint(ticket)

    from app.views.message import bp as message
    app.register_blueprint(message)

    from app.views.test import bp as test
    app.register_blueprint(test)

    return app
