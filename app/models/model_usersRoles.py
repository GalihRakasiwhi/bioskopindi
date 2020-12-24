from app.extensions._db import db
#from app.models.users import UsersModel
#from app.models.roles import RolesModel


class UserRolesModel(db.Model):
    __tablename__ = 'tblUserRoles'

    user_id = db.Column(db.Integer, db.ForeignKey('tblUsers.id'),nullable=False, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('tblRoles.id'),nullable=False, primary_key=True)


    def __repr(self):
        return f"<UserRolesModel {self.full_name}>"
