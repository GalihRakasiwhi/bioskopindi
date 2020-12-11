from app.extensions._db import db


class CompanyModel(db.Model):
    __tablename__ = 'tblCompanys'
    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(128), unique=True, nullable=False)
    company_address = db.Column(db.Text)
    company_descrption = db.Column(db.Text)
    company_income = db.Column(db.Float)

    def __repr(self):
        return f"<Company {self.full_name}>"
