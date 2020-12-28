from app.extensions._db import db

class BookingTicketModel(db.Model):
    __tablename__ = 'tblBookingTicket'
    id = db.Column(db.Integer, primary_key=True)
    bticket_user_id = db.Column(db.Integer, db.ForeignKey('tblUsers.id'), nullable=False)
    #bticket_movie_id = db.Column(db.Integer, db.ForeignKey('tblMovies.id'), nullable=False)
    bticket_schedule_id = db.Column(db.Integer, db.ForeignKey('tblSchedules.id'), nullable=False)
    bticket_seats_number = db.Column(db.Text, nullable=False)
    bticket_price = db.Column(db.Float, nullable=False)
    bticket_status = db.Column(db.Integer, db.ForeignKey('tblPaymentStatus.id'), nullable=False)
    bticket_added = db.Column(db.DateTime, nullable=False)
    bticket_message = db.relationship('MessageToSystemModel', backref='tblBookingTicket', lazy=True)

    def __repr(self):
        return f"<BookingTicketModel {self.id}>"
