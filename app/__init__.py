import os

from flask import Flask


def create_app():
    app = Flask(__name__)
    # config
    app.config.from_object(os.environ['APP_CONFIG_FILE'])

    # extension
    from .extensions._db import db, setup_db
    setup_db(app)

    # view
    from app.views.auths import bp as auth
    app.register_blueprint(auth)

    return app
