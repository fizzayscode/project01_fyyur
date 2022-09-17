from flask import Flask 
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime as datetime





app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)

migrate =Migrate(app,db)

app.config['SQLALCHEMY_DATABASE_URI']="postgresql://postgres:password@localhost:5432/fyyurapp"

# TODO: connect to a local postgresql database

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)) ,nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link=db.Column(db.String(500))
    seeking_talent= db.Column(db.Boolean, nullable=False, default=False)
    seeking_description=db.Column(db.String(500))
    shows=db.relationship('Shows',backref='venues', lazy=True)

# artist_show = db.Table('artist_shows',
# db.Column('artist_id',db.Integer,db.ForeignKey('Artist.id'),primary_key=True),
# db.Column('shows_id',db.Integer,db.ForeignKey('shows.id'),primary_key=True)
# )
     

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(db.ARRAY(db.String(120)) ,nullable=False)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website_link=db.Column(db.String(500))
    seeking_venue= db.Column(db.Boolean, nullable=False, default=False)
    seeking_description=db.Column(db.String(500))
    # shows =db.relationship('Shows',secondary=artist_show, backref=db.backref('artists'),lazy=True)

    shows=db.relationship('Shows',backref='artists', lazy=True)


    # TODO: implement any missing fields, as a database migration using Flask-Migrate

# TODO Implement Show and Artist models, and complete all model relationships and properties, 
# as a database migration.
    
class Shows(db.Model):
      __tablename__='shows'
      id=db.Column(db.Integer,primary_key=True ,nullable=False) 
      venue_id=db.Column(db.Integer, db.ForeignKey('Venue.id'))
      artist_id=db.Column(db.Integer, db.ForeignKey('Artist.id'))
      start_time=db.Column(db.DateTime, default = datetime.now)

  