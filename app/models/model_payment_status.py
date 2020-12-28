from app.extensions._db import db


class PaymentStatusModel(db.Model):
    __tablename__ = 'tblPaymentStatus'

    id = db.Column(db.Integer, primary_key=True)
    payment_status = db.Column(db.String(24), nullable=False)
    payment_status_bticket = db.relationship('BookingTicketModel', backref='tblPaymentStatus', lazy=True)

    def __repr(self):
        return f"<PaymentStatusModel {self.id}>"
