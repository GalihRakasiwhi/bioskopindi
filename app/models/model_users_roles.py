from app.extensions._db import db

class UsersRolesModel(db.Model):
    __tablename__ = 'tblUserRoles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('tblUsers.id'),nullable=False, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('tblRoles.id'),nullable=False, primary_key=True)


    def __repr(self):
        return f"<UserRoles {self.id}>"
