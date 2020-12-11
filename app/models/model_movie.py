from app.extensions._db import db
#from app.models.model_ticket import TicketModel

class MovieModel(db.Model):
    __tablename__ = 'tblMovies'
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(128), nullable=False)
    movie_img_url = db.Column(db.String(255))
    #movie_country = db.Column(db.String(64))
    movie_duration = db.Column(db.Integer)
    #movie_genre = db.Column(db.String(128))
    movie_description = db.Column(db.Text)
    movie_onshow = db.Column(db.Boolean, nullable=False)
    movie_upcoming = db.Column(db.Boolean, nullable=False)
    movie_sold_ticket = db.Column(db.Integer)
    movie_released = db.Column(db.Date, nullable=False)
    movie_edited = db.Column(db.DateTime)
    movie_added = db.Column(db.DateTime, nullable=False)
    movie_schedule = db.relationship('ScheduleModel', backref='tblMovies', lazy=True)

    def __repr(self):
        return f"<Movie {self.movie_title}>"


class StudioModel(db.Model):
    __tablename__ = 'tblStudio'
    id = db.Column(db.Integer, primary_key=True)
    studio_name = db.Column(db.String(128), nullable=False, unique=True)
    studio_capacity = db.Column(db.Integer, nullable=False)
    studio_description = db.Column(db.Text)
    studio_schedule = db.relationship('ScheduleModel', backref='tblStudio', lazy=True)

    def __repr(self):
        return f"<Movie {self.id}>"


class ScheduleModel(db.Model):
    __tablename__ = 'tblSchedules'
    id = db.Column(db.Integer, primary_key=True)
    schedule_movie_id = db.Column(db.Integer, db.ForeignKey('tblMovies.id'), nullable=False)
    schedule_studio_id = db.Column(db.Integer, db.ForeignKey('tblStudio.id'), nullable=False)
    schedule_start_date = db.Column(db.Date, nullable=False)
    schedule_end_date = db.Column(db.Date, nullable=False)
    schedule_time = db.Column(db.Time, nullable=True)
    schedule_ticket = db.relationship('TicketModel', backref='tblSchedules', lazy=True)
    schedule_added = db.Column(db.DateTime, nullable=False)

    def __repr(self):
        return f"<Movie {self.id}>"
