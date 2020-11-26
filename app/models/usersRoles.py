from app.extensions._db import db


class UsersRolesModel(db.Model):
    __tablename__ = 'tblUsersRoles'

    users_id = db.Column(db.Integer, primary_key=True)
    roles_id = db.Column(db.Integer, primary_key=True)

    def __repr(self):
        return f"<UsersRoles {self.full_name}>"
