import json
from flask import Flask,render_template,request,redirect,flash,url_for
from config import Config, DevelopmentConfig
from datetime import datetime


MAX_BOOKING = 12


def loadClubs():
    with open('clubs.json') as c:
         listOfClubs = json.load(c)['clubs']
         return listOfClubs


def loadCompetitions():
    with open('competitions.json') as comps:
         listOfCompetitions = json.load(comps)['competitions']
         return listOfCompetitions


def update_competitions_places(competitions_data, competition):
    competitions_file = open("competitions.json", "w")
    for d in competitions_data:
        if d['name'] == competition['name']:
            d['numberOfPlaces'] = str(competition['numberOfPlaces'])
    json.dump({'competitions':competitions_data}, competitions_file, indent=4)


def update_club_points_balance(clubs_data, club):
    club_file = open("clubs.json", "w")
    for d in clubs_data:
        if d['name'] == club['name']:
            d['points'] = str(club['points'])
    json.dump({'clubs':clubs_data}, club_file, indent=4)


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


@app.route('/showSummary',methods=['GET','POST'])
def showSummary():
    club = search_club_by_email(clubs, email=request.form['email'])
    if not club:
        message = "Sorry, that email wasn't found."
        flash(message)
        return render_template('index.html'), 401
    else:
        return render_template('welcome.html',club=club, competitions=competitions)

@app.route('/pointsDisplayBoard')
def displayClubPoints():
    clubs = loadClubs()
    return render_template('display_clubs.html',clubs=clubs)

def search_club_by_name(clubs, name):
    found_club = None
    for club in clubs:
        if club['name'] == name:
            found_club = club
            break
    return found_club


def search_competition_by_name(competitions, name):
    found_competition = None
    for competition in competitions:
        if competition['name'] == name:
            found_competition = competition
            break
    return found_competition


@app.route('/book/<competition>/<club>')
def book(competition,club):
    clubs = loadClubs()
    competitions = loadCompetitions()
    foundClub = search_club_by_name(clubs, name=club)
    foundCompetition = search_competition_by_name(competitions, name=competition)
    if foundClub and foundCompetition:
        return render_template('booking.html',club=foundClub,competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template('welcome.html', club=club, competitions=competitions)


def club_points_substrations(club, clubPoints, placesRequired):
    club['points'] = clubPoints - placesRequired
    return club['points']


def is_past_competition(competition):
    competition_date = competition["date"]
    competition_date = datetime.strptime(
    competition_date,
    "%Y-%m-%d %H:%M:%S")
    now = datetime.now()
    if competition_date < now : 
        return True
    return False


@app.route('/purchasePlaces',methods=['POST'])
def purchasePlaces():
    clubs = loadClubs()
    competitions = loadCompetitions()
    club = search_club_by_name(clubs, name=request.form['club'])
    competition = search_competition_by_name(competitions, request.form['competition'])
    placesRequired = int(request.form['places'])
    availablesCompetitionPlaces = int(competition['numberOfPlaces'])
    clubPoints = int(club['points'])
    if placesRequired > availablesCompetitionPlaces:
        message = "You can't book more places than availables competition places : " + str(availablesCompetitionPlaces)
        flash(message)
        return render_template('booking.html',club=club,competition=competition), 405
    elif placesRequired > clubPoints:
        message = "You have " + str(clubPoints) + " points which is not enough to book " + str(placesRequired) + " places." 
        flash(message)
        return render_template('booking.html',club=club,competition=competition), 405
    elif placesRequired <= 0:
        message = "Booking a negative number of places or 0 is forbidden."
        flash(message)
        return render_template('booking.html',club=club,competition=competition), 405
    elif placesRequired > MAX_BOOKING:
        message = "Booking more than " + str(MAX_BOOKING) + " places is forbidden."
        flash(message)
        return render_template('booking.html',club=club,competition=competition), 405
    elif is_past_competition(competition):
        message = "Booking a past competition is forbidden."
        flash(message)
        return render_template('booking.html',club=club,competition=competition), 405
    else:
        competition['numberOfPlaces'] = availablesCompetitionPlaces - placesRequired
        club['points'] = club_points_substrations(club, clubPoints, placesRequired)
        competitions_data = loadCompetitions()
        clubs_data = loadClubs()
        update_competitions_places(competitions_data, competition)
        update_club_points_balance(clubs_data, club)
        flash('Great-booking complete!')
        return render_template('welcome.html', club=club, competitions=competitions)


@app.route('/logout')
def logout():
    return redirect(url_for('index'))


    