from sqlalchemy import Column, String, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os

database_path = os.environ['DATABASE_URL']
#comment the upper line and decomment below if you have troubles while testing
database_path="postgres://postgres:postgres@localhost:5432/capstone"
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'Movie'
    id = Column(db.Integer, primary_key=True)
    title = Column(db.String, nullable=False)
    release_date = Column(db.DateTime)
    actors = db.relationship("Actor", secondary='actor_movie', back_populates='movies' )

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release date': self.release_date}

    def __repr__(self):
        return self.format()


class Actor(db.Model):
    __tablename__ = 'Actor'

    id = Column(db.Integer, primary_key=True)
    name = Column(db.String, nullable=False)
    # date of birth
    dob = Column(db.DateTime, nullable=False)
    gender = Column(db.String)
    movies = db.relationship("Movie", secondary="actor_movie", back_populates="actors")

    def __init__(self, name, dob, gender):
        self.name = name
        self.dob = dob
        self.gender = gender

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'DOB': self.dob,
            'gender': self.gender
        }

    def __repr__(self):
        return self.format()


# Assosiation table many to many
actor_movie = db.Table(
    "actor_movie",
    db.Column("actor_id", db.Integer, db.ForeignKey(
        "Actor.id"), primary_key=True),
    db.Column("movie_id", db.Integer, db.ForeignKey(
        "Movie.id"), primary_key=True),
)
