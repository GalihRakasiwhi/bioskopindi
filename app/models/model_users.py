from app.extensions._db import db
from flask_login import UserMixin

class UsersModel(UserMixin, db.Model):
    __tablename__ = 'tblUsers'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(512),nullable=False)
    user_point = db.Column(db.Integer)
    user_booking = db.relationship('BookingTicketModel', backref='tblUsers', lazy=True)
    user_konfirmasi = db.relationship('MessageToSystemModel', backref='tblUsers', lazy=True)
    user_role = db.relationship('UsersRolesModel', backref='tblUsers', lazy=True)

    def __repr(self):
        return f"<UsersModel {self.full_name}>"
