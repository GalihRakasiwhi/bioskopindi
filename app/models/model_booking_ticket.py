from app.extensions._db import db

class BookingTicketModel(db.Model):
    __tablename__ = 'tblBuyTicket'
    id = db.Column(db.Integer, primary_key=True)
    bticket_id_movie = db.Column(db.Integer)
    bticket_id_schedule = db.Column(db.Integer)
    bticket_seat_number = db.Column(db.Text, nullable=False)
    bticket_payment = db.Column(db.Float, nullable=False)
    bticket_status = db.Column(db.String, nullable=False)
    bticket_added = db.Column(db.DateTime, nullable=False)

    def __repr(self):
        return f"<BookingTicketModel {self.id}>"
