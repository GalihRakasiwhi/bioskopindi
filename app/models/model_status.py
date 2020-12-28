from app.extensions._db import db


class StatusModel(db.Model):
    __tablename__ = 'tblStatus'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(12), nullable=False)
    status_ticket = db.relationship('TicketModel', backref='tblStatus', lazy=True)
    #status_message = db.relationship('MessageToSystemModel', backref='tblStatus', lazy=True)

    def __repr(self):
        return f"<StatusModel {self.id}>"
