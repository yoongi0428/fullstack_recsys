from app import db

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    age = db.Column(db.Integer, nullable=False, default=-1)
    gender = db.Column(db.String(10), nullable=False, default='-')
    movies = db.relationship('Interaction', back_populates='user')

    def __repr__(self):
        return "<user '{}'>".format(self.id)


class Movie(db.Model):
    __tablename__ = "Movie"

    id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    title = db.Column(db.String(50))
    genre = db.Column(db.String(50))
    date = db.Column(db.Date)
    users = db.relationship('Interaction', back_populates='movie')
    poster = db.Column(db.String(100))

    def __repr__(self):
        return "<movie '{}'>".format(self.title)

class Interaction(db.Model):
    __tablename__ = "Interaction"

    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), primary_key=True)
    movie_id = db.Column(db.String(50),db.ForeignKey('Movie.id'), primary_key=True)
    rating = db.Column(db.Integer)  
    timestamp =db.Column(db.Integer, nullable=True)
    user = db.relationship('User', back_populates='movies')
    movie = db.relationship('Movie', back_populates='users')

    def __repr__(self):
        return "<User {} - Movie {} - Rating {}>".format(self.user.id, self.movie.title, self.rating)