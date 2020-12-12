from app.extensions._db import db
#from app.models.model_movie import ScheduleModel

class TicketModel(db.Model):
    __tablename__ = 'tblTicket'
    id = db.Column(db.Integer, primary_key=True)
    ticket_code = db.Column(db.String(128), unique=True, nullable=False)
    ticket_user = db.Column(db.Integer, db.ForeignKey('tblUsers.id'), nullable=False)
    ticket_schedule = db.Column(db.Integer, db.ForeignKey('tblSchedules.id'), nullable=False)
    ticket_seat_number = db.Column(db.Integer, nullable=False)

    def __repr(self):
        return f"<BookingTicket {self.id}>"
