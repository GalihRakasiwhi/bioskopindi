from app.extensions._db import db


class MovieModel(db.Model):
    __tablename__ = 'tblMovies'
    id = db.Column(db.Integer, primary_key=True)
    movie_title = db.Column(db.String(128), nullable=False)
    movie_img_url = db.Column(db.String(255))
    #movie_country = db.Column(db.String(64))
    movie_duration = db.Column(db.String(24))
    #movie_genre = db.Column(db.String(128))
    movie_descrption = db.Column(db.Text)
    movie_onshow = db.Column(db.Boolean, nullable=False)
    movie_upcoming = db.Column(db.Boolean, nullable=False)
    movie_sold_ticket = db.Column(db.Integer)
    #movie_income = db.Column(db.Float)
    movie_released = db.Column(db.DateTime)
    movie_added = db.Column(db.DateTime)

    def __repr(self):
        return f"<Movie {self.full_name}>"
