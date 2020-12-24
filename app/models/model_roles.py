from app.extensions._db import db


class RolesModel(db.Model):
    __tablename__ = 'tblRoles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64), unique=True, nullable=False)
    role_user = db.relationship('UsersRolesModel', backref='tblRoles', lazy=True)

    def __repr(self):
        return f"<RolesModel {self.id}>"
