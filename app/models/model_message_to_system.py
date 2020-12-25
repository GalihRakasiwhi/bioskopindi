from app.extensions._db import db

class MessageToSystemModel(db.Model):
    __tablename__ = 'tblMessageToSystem'
    id = db.Column(db.Integer, primary_key=True)
    message_user_id = db.Column(db.Integer, db.ForeignKey('tblUsers.id'),nullable=False)
    message_type = db.Column(db.String(128), nullable=False)
    message_text = db.Column(db.Text)
    message_img_url = db.Column(db.String(255))
    message_status = db.Column(db.String(128), nullable=False)
    message_send_time = db.Column(db.DateTime, nullable=False)

    def __repr(self):
        return f"<MessageToSystemModel {self.id}>"
