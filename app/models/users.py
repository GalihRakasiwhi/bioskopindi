from app.extensions._db import db


class UsersModel(db.Model):
    __tablename__ = 'tblUsers'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(512),nullable=False)


    def __repr(self):
        return f"<Users {self.full_name}>"
