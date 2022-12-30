import json, os
from flask import Flask,render_template,request,redirect,flash,url_for
from config import Config, DevelopmentConfig


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


app = Flask(__name__)
app.secret_key = 'something_special'
# app.config.from_object(DevelopmentConfig)
app.config.update(TESTING=True, DEBUG=True)

competitions = loadCompetitions()
clubs = loadClubs()

@app.route('/')
def index():
    return render_template('index.html')


def search_club_by_email(clubs, email):
    found_club = None
    for club in clubs:
        if club['email'] == email:
            found_club = club
            break
    return found_club
@app.route('/showSummary',methods=['POST'])


def showSummary():
    clubs = loadClubs()
    club = search_club_by_email(clubs, email=request.form['email'])
    if not club:
        message = "Sorry, that email wasn't found."
        flash(message)
        return render_template('index.html'), 401
    else:
        return render_template('welcome.html',club=club,competitions=competitions)
    
 
@app.route('/book/<competition>/<club>')
def book(competition,club):
    foundClub = [c for c in clubs if c['name'] == club][0]
    foundCompetition = [c for c in competitions if c['name'] == competition][0]
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    competition = [c for c in competitions if c['name'] == request.form['competition']][0]
    club = [c for c in clubs if c['name'] == request.form['club']][0]
    placesRequired = int(request.form['places'])
    competition['numberOfPlaces'] = int(competition['numberOfPlaces'])-placesRequired
    flash('Great-booking complete!')
    return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


# TODO: 
# Add route for points display

    