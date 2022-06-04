from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

db = SQLAlchemy()
migrate = Migrate()

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False, unique=True)
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500), unique=True)
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_talent = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text())
    shows = db.relationship('Show', backref='venue', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    def all_venue_details(self):
        all_shows = []
        for show in self.shows:
            all_shows.append(
                Show.show_artist(Show.query.get(show.id))
            )
        genres = json.loads(self.genres)
        data = {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'address': self.address,
            'phone': self.phone,
            'facebook_link': self.facebook_link,
            'website': self.website,
            'image_link': self.image_link,
            'seeking_talent': self.seeking_talent,
            'seeking_description': self.seeking_description,
            'genres': genres,
            'all_shows': all_shows
        }

        return data


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    city = db.Column(db.String(120), nullable=False)
    state = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(120), nullable=False)
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500), unique=True)
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(500))
    seeking_venue = db.Column(db.Boolean, default=False)
    seeking_description = db.Column(db.Text())
    shows = db.relationship('Show', backref='artist', lazy=True)

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

    def all_artist_details(self):
        all_shows = []
        for show in self.shows:
            all_shows.append(
                Show.show_venue(Show.query.get(show.id))
            )
        genres = json.loads(self.genres)

        data = {
            'id': self.id,
            'name': self.name,
            'city': self.city,
            'state': self.state,
            'phone': self.phone,
            'website': self.website,
            'image_link': self.image_link,
            'facebook_link': self.facebook_link,
            'genres': genres,
            'seeking_venue': self.seeking_venue,
            'seeking_description': self.seeking_description,
            'all_shows': all_shows
        }

        return data


class Show(db.Model):
    __tablename__ = 'Show'
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id', ondelete="CASCADE"), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id', ondelete="CASCADE"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    def show_artist(self):
        the_artist = Artist.query.get(self.artist_id)
        return {
            'artist_id': the_artist.id,
            'artist_name': the_artist.name,
            'artist_image_link': the_artist.image_link,
            'start_time': self.start_time.strftime("%Y/%m/%d, %H:%M:%S")
        }

    def show_venue(self):
        the_venue = Venue.query.get(self.venue_id)
        return {
            'venue_id': the_venue.id,
            'venue_name': the_venue.name,
            'venue_image_link': the_venue.image_link,
            'start_time': self.start_time.strftime("%Y/%m/%d, %H:%M:%S")
        }
