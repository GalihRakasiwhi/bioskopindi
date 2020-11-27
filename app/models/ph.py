from app.extensions._db import db


class PhModel(db.Model):
    __tablename__ = 'tblPh'
    id = db.Column(db.Integer, primary_key=True)
    ph_name = db.Column(db.String(128), unique=True, nullable=False)
    ph_address = db.Column(db.Text)
    ph_descrption = db.Column(db.Text)
    ph_income = db.Column(db.Float)

    def __repr(self):
        return f"<Ph {self.full_name}>"
