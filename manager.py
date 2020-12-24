from sqlalchemy.orm import relationship, backref

from app import create_app
from app.extensions._db import db
from app.models.model_users import UsersModel
from app.models.model_roles import RolesModel
from app.models.model_users_roles import UsersRolesModel
#from app.models.model_users_admin import UsersAdminModel
from app.models.model_movie import MovieModel, StudioModel, ScheduleModel
from app.models.model_ticket import TicketModel
from app.models.model_booking_ticket import BookingTicketModel
from app.models.model_message_to_system import MessageToSystemModel

app = create_app()


def migrate_all():
    db.create_all()

    #check if tbl role is null
    if not db.session.query(db.exists().where(RolesModel.role == 'Admin')).scalar():
    	roles = RolesModel(role = 'Admin')
    	db.session.add(roles)
    	db.session.commit()
    	print('Role Admin added')

    if not db.session.query(db.exists().where(RolesModel.role == 'User')).scalar():
    	roles = RolesModel(role = 'User')
    	db.session.add(roles)
    	db.session.commit()
    	print('Role User added')


if __name__ == '__main__':
    with app.app_context():
        migrate_all()
