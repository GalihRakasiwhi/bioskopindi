from app.extensions._db import db


class RolesModel(db.Model):
    __tablename__ = 'tblRoles'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64), unique=True, nullable=False)
    #userrole = relationship('UserRolesModel', backref='role', lazy=True)

    def __repr(self):
        return f"<Roles {self.full_name}>"
