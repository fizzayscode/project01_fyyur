#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

from concurrent.futures.process import _python_exit
from ctypes import addressof
from distutils.log import error
from email.policy import default
import json
from os import abort
import sys
from xmlrpc.client import Boolean, DateTime
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from pyparsing import with_attribute
from sqlalchemy import PrimaryKeyConstraint
from forms import *
# from flask_migrate import Migrate
from models import *

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#




#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues data.
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.
  venues=Venue.query.all()
 
  
  data=[]
    # iterating over the whole venues to get some data to display
  for venue in venues:

    # trying to get all the shows in a particular venue based on the particlar venue_id which is a foreign key
    shows= Shows.query.filter_by(venue_id=venue.id)

    # filtering the shows i got in a particular venue based on the start_time and then counting
    num=(shows.filter(Shows.start_time > datetime.now())).count()

    
    needs={
        "city":venue.city,
        "state":venue.state,
        "venues":[{
          "id": venue.id,
          "name":venue.name,
          "num_upcoming_shows":num
        }]
      }
    data.append(needs)
    
   
  # data= [{
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "venues": [{
  #     "id": 1,
  #     "name": "The Musical Hop",
  #     "num_upcoming_shows": 0,
  #   }, {
  #     "id": 3,
  #     "name": "Park Square Live Music & Coffee",
  #     "num_upcoming_shows": 1,
  #   }]
  # }, {
  #   "city": "New York",
  #   "state": "NY",
  #   "venues": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }]

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  search= request.form.get('search_term')
  venues= Venue.query.filter(Venue.name.ilike("%"+search+"%")).all()
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  data=[]
    
  for venue in venues: 
    # get the number of shows in this particular venue id
    shows= Shows.query.filter_by(id=venue.id)

   
    num_of_shows= shows.filter(Shows.start_time > datetime.now())
    length_of_shows = num_of_shows.count()

    needs={
        "id":venue.id,
        "name":venue.name,
        "num_upcoming_shows":length_of_shows
        
        }
      
    data.append(needs)

    response={
      "count":len(data),
      "data":data
    }
    
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 2,
  #     "name": "The Dueling Pianos Bar",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues table, using venue_id
  venue=Venue.query.get(venue_id)

 

# filtering the shows in a particular venue
  shows=Shows.query.filter_by(venue_id=venue_id)

  for show in shows: 
   artist=Artist.query.filter_by(id=show.artist_id).first()

   artist_each={
      "artist_id":show.artist_id,
      "artist_name":artist.name,
      "artist_image_link":artist.image_link,
      "start_time":str(show.start_time)
    }
  past_shows_query=db.session.query(Shows).join(Venue).filter(Shows.venue_id==venue_id).filter(Shows.start_time<datetime.now()).all()
  past_shows=[]

  upcoming_shows_query=db.session.query(Shows).join(Venue).filter(Shows.venue_id==venue_id).filter(Shows.start_time<datetime.now()).all()
  upcoming_shows=[]

    # trying to figure out every artist in a particular show in a venue
 

  for show in past_shows_query:
    past_shows.append(artist_each)
  
  for show in upcoming_shows_query:
    upcoming_shows.append(artist_each)

    #  if show.start_time<=datetime.now():
    #   past_shows.append(artist_each)
    #  else:
    #   upcoming_shows.append(artist_each)


  

  # shows=Shows.query.filter_by(id=venue_id)
  
  data1={
    "id":venue.id,
    "name":venue.name,
    "genres":[venue.genres],
    "address": venue.address,
    "city":venue.city,
    "state":venue.state,
    "phone":venue.phone,
    "website":venue.website_link,
    "facebook_link":venue.facebook_link,
    "seeking_talent":venue.seeking_talent,
    "seeking_description":venue.seeking_description,
    "image_link": venue.image_link,
    "past_shows":past_shows,
    "upcoming_shows":upcoming_shows
  }
  
  # data1={
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #   "past_shows": [{
  #     "artist_id": 4,
  #     "artist_name": "Guns N Petals",
  #     "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 2,
  #   "name": "The Dueling Pianos Bar",
  #   "genres": ["Classical", "R&B", "Hip-Hop"],
  #   "address": "335 Delancey Street",
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "914-003-1132",
  #   "website": "https://www.theduelingpianos.com",
  #   "facebook_link": "https://www.facebook.com/theduelingpianos",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 3,
  #   "name": "Park Square Live Music & Coffee",
  #   "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
  #   "address": "34 Whiskey Moore Ave",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "415-000-1234",
  #   "website": "https://www.parksquarelivemusicandcoffee.com",
  #   "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
  #   "seeking_talent": False,
  #   "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #   "past_shows": [{
  #     "artist_id": 5,
  #     "artist_name": "Matt Quevedo",
  #     "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [{
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "artist_id": 6,
  #     "artist_name": "The Wild Sax Band",
  #     "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 1,
  # }
  data = list(filter(lambda d: d['id'] == venue_id, [data1]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm(request.form)
  if form.validate():
    error=False
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion

    try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      address = request.form.get('address')
      phone = request.form.get('phone')
      genres = request.form.getlist('genres')
      facebook_link =request.form.get('facebook_link')
      website_link =request.form.get('website_link')
      seeking_talent=Boolean(request.form.get('seeking_talent'))
      seeking_description = request.form.get('seeking_description')

      venue= Venue(name=name ,city=city ,state=state ,address=address ,phone=phone,
                     genres=genres ,facebook_link=facebook_link ,website_link=website_link,
                     seeking_talent=seeking_talent, seeking_description=seeking_description)
      

      db.session.add(venue)
      db.session.commit()

    except:
        error = True
        db.session.rollback()
        print(sys.exc_info())
    
    finally:
        db.session.close()           

    if error: 
     flash('An error occured.' 'Venue ' + request.form['name'] + ' could not be listed')
  # on successful db insert, flash success
 
  # #TODO: on unsuccessful db insert, flash an error instead.
    else:
        flash('Venue ' + request.form['name'] + ' was successfully listed!') 
    return render_template('pages/home.html')
  # e.g., flash('An error occurred. Venue ' + data.name + ' could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/

  else:
    for field, message in form.errors.items():
            flash(field + ' - ' + str(message), 'danger')
            return render_template('forms/new_venue.html', form=form)
   

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  error=False

  try:
    venue=Venue.query.get(venue_id)
    db.session.delete(venue)
    db.session.commit()


  except:
    error=True
    db.session.rollback()

  finally:
    db.session.close()

  # TODO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return redirect(url_for('index'))

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # data=Artist.query.with_entities(Artist.name,Artist.phone)
  # TODO: replace with real data returned from querying the database
  artists=Artist.query.all()
  data=[]

  for artist in artists:
    need={
      "id":artist.id,
      "name":artist.name
    }
    data.append(need)

  # data=[{
  #   "id": 4,
  #   "name": "Guns N Petals",
  # }, {
  #   "id": 5,
  #   "name": "Matt Quevedo",
  # }, {
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  # }]
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term= request.form.get('search_term')
  artists= Artist.query.filter(Artist.name.ilike("%"+search_term+"%")).all()
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"

  data=[]
    
  for artist in artists:
    show= Artist.query.filter_by(id=artist.id)

    needs={

        "id":artist.id,
        "name":artist.name

        }
      
    data.append(needs)


    response={

      "count":len(data),
      "data":data
    }

  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id
  artist=Artist.query.get(artist_id)

  past_shows=[]
  upcoming_shows=[]

  # trying to get the shows that macth the current artist_id 
  shows=Shows.query.filter_by(artist_id = artist_id)

  for show in shows:
     venue=Venue.query.filter_by(id=show.venue_id).first()

     artist_each={
      "venue_id":venue.id,
      "venue_name":venue.name,
      "venue_image_link":venue.image_link,
      "start_time":str(show.start_time)
    }
  past_shows_query=db.session.query(Shows).join(Artist).filter(Shows.artist_id==artist_id).filter(Shows.start_time<datetime.now()).all()
  past_shows=[]

  upcoming_shows_query=db.session.query(Shows).join(Artist).filter(Shows.artist_id==artist_id).filter(Shows.start_time<datetime.now()).all()
  upcoming_shows=[]

  for show in past_shows_query:
    past_shows.append(artist_each)
  
  for show in upcoming_shows_query:
    upcoming_shows.append(artist_each)





  data1= {
    "id":artist.id,
    "name":artist.name,
    "genres":artist.genres,
    "city":artist.city,
    "state":artist.state,
    "phone":artist.phone,
    "website":artist.website_link,
    "facebook_link":artist.facebook_link,
    "seeking_venue":artist.seeking_venue,
    "seeking_description":artist.seeking_description,
    "image_link":artist.image_link,
     "past_shows":past_shows,
     "upcoming_shows":upcoming_shows,
     "past_shows_count":len(past_shows),
     "upcoming_shows_count":len(upcoming_shows)

  }


  # data1={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "past_shows": [{
  #     "venue_id": 1,
  #     "venue_name": "The Musical Hop",
  #     "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
  #     "start_time": "2019-05-21T21:30:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data2={
  #   "id": 5,
  #   "name": "Matt Quevedo",
  #   "genres": ["Jazz"],
  #   "city": "New York",
  #   "state": "NY",
  #   "phone": "300-400-5000",
  #   "facebook_link": "https://www.facebook.com/mattquevedo923251523",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "past_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2019-06-15T23:00:00.000Z"
  #   }],
  #   "upcoming_shows": [],
  #   "past_shows_count": 1,
  #   "upcoming_shows_count": 0,
  # }
  # data3={
  #   "id": 6,
  #   "name": "The Wild Sax Band",
  #   "genres": ["Jazz", "Classical"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "432-325-5432",
  #   "seeking_venue": False,
  #   "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "past_shows": [],
  #   "upcoming_shows": [{
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-01T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-08T20:00:00.000Z"
  #   }, {
  #     "venue_id": 3,
  #     "venue_name": "Park Square Live Music & Coffee",
  #     "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
  #     "start_time": "2035-04-15T20:00:00.000Z"
  #   }],
  #   "past_shows_count": 0,
  #   "upcoming_shows_count": 3,
  # }
  data = list(filter(lambda d: d['id'] == artist_id, [data1]))[0]
  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):

  form = ArtistForm()
  artist=Artist.query.get(artist_id)

  form.name.data=artist.name
  form.genres.data=artist.genres
  form.city.data=artist.city
  form.state.data=artist.state
  form.phone.data=artist.phone
  form.website_link.data=artist.website_link
  form.facebook_link.data=artist.facebook_link
  form.seeking_venue.data=artist.seeking_venue
  form.seeking_description.data=artist.seeking_description
  form.image_link.data=artist.image_link



  # artist={
  #   "id": 4,
  #   "name": "Guns N Petals",
  #   "genres": ["Rock n Roll"],
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "326-123-5000",
  #   "website": "https://www.gunsnpetalsband.com",
  #   "facebook_link": "https://www.facebook.com/GunsNPetals",
  #   "seeking_venue": True,
  #   "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
  #   "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  # }
  # TODO: populate form with fields from artist with ID <artist_id>
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing
  # artist record with ID <artist_id> using the new attributes
   error=False

   artist=Artist.query.filter_by(id=artist_id).first()

   try:
      artist.name = request.form.get('name')
      artist.city = request.form.get('city')
      artist.state = request.form.get('state')
      artist.address = request.form.get('address')
      artist.phone = request.form.get('phone')
      artist.genres = request.form.getlist('genres')
      artist.facebook_link =request.form.get('facebook_link')
      artist.website_link =request.form.get('website_link')
      artist.seeking_talent=Boolean(request.form.get('seeking_talent'))
      artist.seeking_description = request.form.get('seeking_description') 

      db.session.add(artist)

      db.session.commit()

   except:
    error=True
    db.session.rollback()

   finally:
    db.session.close()

   if error:
    flash('an error occured')
   else: 
    return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue= Venue.query.get(venue_id)

  # setting my form with the predefined data of the venue with venue_id for updating

  form.name.data=venue.name
  form.genres.data=venue.genres
  form.address.data=venue.address
  form.city.data=venue.city
  form.state.data=venue.state
  form.phone.data=venue.phone
  form.website_link.data=venue.website_link
  form.facebook_link.data=venue.facebook_link
  form.seeking_talent.data=venue.seeking_talent
  form.seeking_description.data=venue.seeking_description
  form.image_link.data=venue.image_link
  # venue=Venue.query.filter_by(venue_id)
  # venue= {
  #   "id": 1,
  #   "name": "The Musical Hop",
  #   "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
  #   "address": "1015 Folsom Street",
  #   "city": "San Francisco",
  #   "state": "CA",
  #   "phone": "123-123-1234",
  #   "website": "https://www.themusicalhop.com",
  #   "facebook_link": "https://www.facebook.com/TheMusicalHop",
  #   "seeking_talent": True,
  #   "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
  #   "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  # }
  # TODO: populate form with values from venue with ID <venue_id>
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  error=False
  venue=Venue.query.filter_by(id=venue_id).first()

  try:
      venue.name = request.form.get('name')
      venue.city = request.form.get('city')
      venue.state = request.form.get('state')
      venue.address = request.form.get('address')
      venue.phone = request.form.get('phone')
      venue.genres = request.form.getlist('genres')
      venue.facebook_link =request.form.get('facebook_link')
      venue.website_link =request.form.get('website_link')
      venue.seeking_talent=Boolean(request.form.get('seeking_talent'))
      venue.seeking_description = request.form.get('seeking_description') 


      db.session.add(venue)
      db.session.commit()

  except:
    error=True
    db.session.rollback()

  finally:
    db.session.close()

  if error:
    flash('an error occured')
  else:
     return redirect(url_for('show_venue', venue_id=venue_id))
 # TODO: take values from the form submitted, and update existing
  # venue record with ID <venue_id> using the new attributes
 
 

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm(request.form)
  form.validate()

  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead
  # TODO: modify data to be the data object returned from db insertion
   error=False

   try:
      name = request.form.get('name')
      city = request.form.get('city')
      state = request.form.get('state')
      phone = request.form.get('phone')
      genres = request.form.getlist('genres')
      image_link = request.form.get('image_link')
      facebook_link =request.form.get('facebook_link')
      website_link =request.form.get('website_link')
      seeking_venue=Boolean(request.form.get('seeking_venue'))
      seeking_description = request.form.get('seeking_description')

      artist= Artist(name=name ,city=city ,state=state ,phone=phone,
                     genres=genres ,image_link=image_link ,facebook_link=facebook_link ,website_link=website_link,
                     seeking_venue=seeking_venue, seeking_description=seeking_description)
      

      db.session.add(artist)
      db.session.commit()

   except:
    error = True
    db.session.rollback()
    print(sys.exc_info())
    
   finally:
      db.session.close()       
  
   if error:
  # on successful db insert, flash success
     flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
   if not error:
  # TODO: on unsuccessful db insert, flash an error instead.
     flash('Artist ' + request.form['name'] + ' was successfully listed!')
   return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data.
  data=[]
  shows=Shows.query.all()

  for show in shows:
    venue=Venue.query.get(show.venue_id)
    artist=Artist.query.get(show.artist_id)
    # show=Shows(venue_id=venue_id,start_time=start_time)
    need={
      "venue_id": venue.id,
      "venue_name":venue.name,
      "artist_id":artist.id,
      "artist_name":artist.name,
      "artist_image_link":artist.image_link,
      "start_time":str(show.start_time)
    }

    data.append(need)



  

  # data=[{
  #   "venue_id": 1,
  #   "venue_name": "The Musical Hop",
  #   "artist_id": 4,
  #   "artist_name": "Guns N Petals",
  #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
  #   "start_time": "2019-05-21T21:30:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 5,
  #   "artist_name": "Matt Quevedo",
  #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
  #   "start_time": "2019-06-15T23:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-01T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-08T20:00:00.000Z"
  # }, {
  #   "venue_id": 3,
  #   "venue_name": "Park Square Live Music & Coffee",
  #   "artist_id": 6,
  #   "artist_name": "The Wild Sax Band",
  #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
  #   "start_time": "2035-04-15T20:00:00.000Z"
  # }]
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm(request.form)
  form.validate()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead


  error=False
  try:
   
    artist_id=request.form.get('artist_id')
    venue_id=request.form.get('venue_id')
    start_time=request.form.get('start_time')

    show =Shows(artist_id=artist_id,venue_id=venue_id,start_time=start_time)
    # artist_obj=Artist.query.filter_by(id=artist_id).first()

    
    
    # show=Shows(venue_id=venue_id,start_time=start_time)
    # show.artists.append(artist_obj)

    db.session.add(show)
    db.session.commit()

  except:
     error=True
     db.session.rollback()
     print(sys.exc_info())

  # on successful db insert, flash success
  if error:
     flash('An error occurred. Show could not be listed.')
  else:

   flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
 
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
