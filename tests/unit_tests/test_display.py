from ..utils import loadClub, loadClubs, loadCompetition
# They should be able to see the list of clubs and their associated current points balance


def test_book_should_load_competition(client):
    """Test if the competition to book is well displayed on page."""
    club = "She Lifts"
    foundClub = loadClub(club) 
    competition = "Freebie Shark" 
    foundCompetition = loadCompetition(competition) 
    response = client.get('/book/'+ competition + '/' + club)
    name = foundCompetition['name']
    date = foundCompetition['date']
    places = foundCompetition['numberOfPlaces']
    expecting_data = "Places available: " + places
    assert expecting_data in response.data.decode('UTF-8')
    assert response.status_code == 200


def test_book_should_failed_load_competition(client):
    """Test if the competition to book is well displayed on page."""
    club = "Unknow club"
    foundClub = loadClub(club) 
    competition = "Freebie Shark" 
    response = client.get('/book/'+ competition + '/' + club)
    content = response.data.decode('UTF-8')
    expecting_data = "Something went wrong-please try again"
    print(content)
    assert expecting_data in response.data.decode('UTF-8')
    assert response.status_code == 200

    
def test_should_display_list_of_clubs(client):
    """Test if the list of clubs well displayed on page."""
    response = client.get('/pointsDisplayBoard')
    clubs = loadClubs()
    for club in clubs:
        name = club['name']
        points = club['points']
        expecting_data = "<li>\n            "+ name + "<br />\n            " + "Points: " + points + "</br>\n        </li>\n"
        assert expecting_data in response.data.decode('UTF-8')
    assert response.status_code == 200


# test don't display page summarry if not authenticated
def test_should_not_display_summarry_if_no_authenticated(client):
    response = client.get('/showSummary')
    assert response.status_code == 403
