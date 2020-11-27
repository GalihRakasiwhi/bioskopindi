from app.extensions._db import db


class BookingTicketModel(db.Model):
    __tablename__ = 'tblBookingTicket'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    movie_name = db.Column(db.String(128), nullable=False)
    seat_number = db.Column(db.Integer, nullable=False)
    date = db.Column(db.String(128), nullable=False)
    time = db.Column(db.String(128), nullable=False)
    studio = db.Column(db.String(128), nullable=False)
    code_ticket = db.Column(db.String(128), nullable=False)

    def __repr(self):
        return f"<BookingTicket {self.full_name}>"
