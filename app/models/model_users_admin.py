from app.extensions._db import db
from flask_login import UserMixin

class UsersAdminModel(UserMixin, db.Model):
    __tablename__ = 'tblUsersAdmin'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(25), unique=True, nullable=False)
    full_name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(512), nullable=False)
    #userrole = relationship('UserRolesModel', backref='user', lazy=True)

    def __repr(self):
        return f"<Users {self.full_name}>"
