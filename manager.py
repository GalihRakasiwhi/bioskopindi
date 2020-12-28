from sqlalchemy.orm import relationship, backref

from app import create_app
from app.extensions._db import db
from app.models.model_users import UsersModel
from app.models.model_roles import RolesModel
from app.models.model_users_roles import UsersRolesModel
#from app.models.model_users_admin import UsersAdminModel
from app.models.model_movie import MovieModel, StudioModel, ScheduleModel
from app.models.model_payment_status import PaymentStatusModel
from app.models.model_ticket import TicketModel
from app.models.model_booking_ticket import BookingTicketModel
from app.models.model_message_to_system import MessageToSystemModel
from app.models.model_status import StatusModel

app = create_app()


def migrate_all():
    db.create_all()

    #check if tbl role is null
    if not db.session.query(db.exists().where(RolesModel.role == 'Admin')).scalar():
    	roles = RolesModel(role = 'Admin')
    	db.session.add(roles)
    	db.session.commit()
    	print('Role "Admin" added')

    if not db.session.query(db.exists().where(RolesModel.role == 'User')).scalar():
    	roles = RolesModel(role = 'User')
    	db.session.add(roles)
    	db.session.commit()
    	print('Role "User" added')


    #check if tbl payment_status is null
    if not db.session.query(db.exists().where(PaymentStatusModel.payment_status == 'Waiting for Payment')).scalar():
        create = PaymentStatusModel(payment_status = 'Waiting for Payment')
        db.session.add(create)
        db.session.commit()
        print('Status "Waiting for Payment" added')

    if not db.session.query(db.exists().where(PaymentStatusModel.payment_status == 'Under Review')).scalar():
        create = PaymentStatusModel(payment_status = 'Under Review')
        db.session.add(create)
        db.session.commit()
        print('Status "Under Review" added')

    if not db.session.query(db.exists().where(PaymentStatusModel.payment_status == 'Payment Confirmed')).scalar():
        create = PaymentStatusModel(payment_status = 'Payment Confirmed')
        db.session.add(create)
        db.session.commit()
        print('Status "Payment Confirmed" added')

    if not db.session.query(db.exists().where(PaymentStatusModel.payment_status == 'Payment Declined')).scalar():
        create = PaymentStatusModel(payment_status = 'Payment Declined')
        db.session.add(create)
        db.session.commit()
        print('Status "PPayment Declined" added')


    #check if tbl status is null
    if not db.session.query(db.exists().where(StatusModel.status == 'unread')).scalar():
        create = StatusModel(status = 'unread')
        db.session.add(create)
        db.session.commit()
        print('Status "unread" added')

    if not db.session.query(db.exists().where(StatusModel.status == 'read')).scalar():
        create = StatusModel(status = 'read')
        db.session.add(create)
        db.session.commit()
        print('Status "read" added')

if __name__ == '__main__':
    with app.app_context():
        migrate_all()
