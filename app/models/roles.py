from app.extensions._db import db


class RolesModel(db.Model):
    __tablename__ = 'tblRole'

    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(64), unique=True, nullable=False)


    def __repr(self):
        return f"<Roles {self.full_name}>"
