from app.extensions._db import db

class UsersRolesModel(db.Model):
    __tablename__ = 'tblUserRoles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tblUsers.id'),nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('tblRoles.id'),nullable=False)


    def __repr(self):
        return f"<UsersRolesModel {self.id}>"
