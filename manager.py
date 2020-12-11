from sqlalchemy.orm import relationship, backref

from app import create_app
from app.extensions._db import db
from app.models.users import UsersModel
from app.models.roles import RolesModel
from app.models.model_users_admin import UsersAdminModel
from app.models.model_movie import MovieModel, StudioModel, ScheduleModel
from app.models.model_ticket import TicketModel

app = create_app()


def migrate_all():
    db.create_all()


if __name__ == '__main__':
    with app.app_context():
        migrate_all()
