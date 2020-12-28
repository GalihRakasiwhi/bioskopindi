from app.extensions._db import db

class TicketModel(db.Model):
    __tablename__ = 'tblTicket'
    id = db.Column(db.Integer, primary_key=True)
    ticket_code = db.Column(db.String(128), unique=True, nullable=False)
    ticket_user = db.Column(db.Integer, db.ForeignKey('tblUsers.id'), nullable=False)
    ticket_schedule = db.Column(db.Integer, db.ForeignKey('tblSchedules.id'), nullable=False)
    ticket_seat_number = db.Column(db.String(12), nullable=False)
    ticket_price = db.Column(db.Float, nullable=False)
    ticket_status = db.Column(db.Integer, db.ForeignKey('tblStatus.id'), nullable=False)
    ticket_added = db.Column(db.DateTime, nullable=False)

    def __repr(self):
        return f"<TicketModel {self.id}>"
