# They should not be able to redeem more points than available; this should be done within the UI. 
# The redeemed points should be correctly deducted from the club's total.
import json

# ecrire une fonction qui ouvre les competitions et recupère les données de la compéitions si il la rtouve; 
def loadCompetition(competition_name):
    with open('competitions.json') as comps:
        listOfCompetitions = json.load(comps)['competitions']
        for comp in listOfCompetitions:
          if comp['name'] == competition_name:
            return comp
        return None


# book with sufficient points balance
def test_sufficient_points_balance_should_return_status_200(client):
    """
    Test club book a competition with sufficient points balance.
    """
    response= client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": "Spring Festival",
      "places": 12
    })
    assert response.status_code == 200


# book with insufficient points balance
def test_insufficient_points_balance_should_return_error(client):
    """
    Test club book a competition with insufficient points balance.
    """
    competition = loadCompetition("Spring Festival")
    required_places = 16
    response= client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": competition['name'],
      "places": required_places
    })
    assert response.status_code == 405
    text_search = "You have " + str(15) + " points which is not enough to book " + str(required_places) + " places."
    print("text_search", text_search)
    print("decode :", response.data.decode('UTF-8'))
    assert text_search in response.data.decode('UTF-8')


# if placesRequired > availablePlaces
def test_required_places_superior_to_available_places_should_return_status_405(client):
    """
    Test club book more places than availables places.
    """
    response= client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": "Fall Classic",
      "places": 11
    })
    assert response.status_code == 405
    # assert "You can't book more places than availables competition places : " in response.data.decode('UTF-8')


def test_book_negative_number_of_places_should_return_error(client):
    """
    Test club book a negative number of places which is impossible.
    """
    response = client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": "Fall Classic",
      "places": -5
    })
    assert response.status_code == 405
    assert "Booking a negative number of places or 0 is forbidden." in response.data.decode('UTF-8')


# substract points from club when club books places
def test_booked_places_should_subtract_club_points(client):
    """
    Test deduction of club points when club books a competition
    with points of club = 15.  
    """
    club_points = 15
    response= client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": "Spring Festival",
      "places": 3
    })
    assert response.status_code == 200
    assert "Points available: " + str(club_points - 3) in response.data.decode('UTF-8')