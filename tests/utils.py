import json
import shutil


def reset_data():
  shutil.copy('tests/datas/competitions.json', 'competitions.json')
  shutil.copy('tests/datas/clubs.json', 'clubs.json')


# load the requested competion object
def loadCompetition(competition_name):
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        for comp in listOfCompetitions:
          if comp['name'] == competition_name:
            return comp
        return None


#  load the requested club object
def loadClub(club_name):
    with open('clubs.json') as clubs:
        listOfClubs = json.load(clubs)['clubs']
        for club in listOfClubs:
          if club['name'] == club_name:
            return club
        return None