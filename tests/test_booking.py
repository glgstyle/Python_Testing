from server import MAX_BOOKING
from .utils import reset_data, loadclub, loadCompetition
# They should not be able to redeem more points than available; this should be done within the UI. 
# The redeemed points should be correctly deducted from the club's total.


# book with sufficient points balance
def test_sufficient_points_balance_should_return_status_200(client):
    """
    Test club book a competition with sufficient points balance.
    """
    reset_data()
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
    reset_data()
    competition = loadCompetition("Spring Festival")
    club = loadclub("She Lifts")
    club_points = club['points']
    required_places = 16
    response= client.post('/purchasePlaces', data={
      "club": club['name'],
      "competition": competition['name'],
      "places": required_places
    })
    assert response.status_code == 405
    expected_text = "You have " + str(club_points) + " points which is not enough to book " + str(required_places) + " places."
    assert expected_text in response.data.decode('UTF-8')


# if placesRequired > availablePlaces
def test_required_places_superior_to_available_places_should_return_status_405(client):
    """
    Test club book more places than availables places.
    """
    reset_data()
    competition = loadCompetition("Fall Classic")
    places_required = 11
    response= client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": competition['name'],
      "places": places_required
    })
    assert response.status_code == 405
    assert "You can&#39;t book more places than availables competition places : " + str(competition['numberOfPlaces']) in response.data.decode('UTF-8')


# negative number
def test_book_negative_number_of_places_should_return_error(client):
    """
    Test club book a negative number of places which is impossible.
    """
    reset_data()
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
    reset_data()
    club = loadclub("She Lifts")
    club_points = int(club['points'])
    places_required = 3
    response= client.post('/purchasePlaces', data={
      "club": club['name'],
      "competition": "Spring Festival",
      "places": places_required,
    })
    assert response.status_code == 200
    assert "Points available: " + str(club_points - places_required) in response.data.decode('UTF-8')


# book more than max determinate places(12)
def test_booking_more_than_max_booking_places_should_return_error(client):
    """
    Test club books more than max_booking places in a competition.
    """
    reset_data()
    response= client.post('/purchasePlaces', data={
      "club": "Simply Lift",
      "competition": "Spring Festival",
      "places": 13
    })
    assert response.status_code == 405
    assert "Booking more than " + str(MAX_BOOKING) + " places is forbidden." in response.data.decode('UTF-8')


# The places are correctly deducted from the competition
def test_booked_places_should_be_subtracted_from_competitions_places(client):
    """
    Test deduction of competition places when club books a competition.  
    """
    reset_data()
    competition = loadCompetition("Spring Festival")
    available_places = int(competition['numberOfPlaces'])
    required_places = 5
    competition_places = available_places
    response= client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": competition['name'],
      "places": required_places
    })
    competition_after = loadCompetition("Spring Festival")
    competition_places_after = int(competition_after['numberOfPlaces'])
    assert response.status_code == 200
    assert competition_places_after == (competition_places - required_places)

# past_competition
def test_book_past_competition_should_return_error(client):
    """
    Test club books places in past competition which is impossible.
    """
    reset_data()
    competition = loadCompetition("Freebie Shark")
    available_competition_places = int(competition['numberOfPlaces']) 
    response = client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": competition['name'],
      "places": 2
    })
    assert response.status_code == 405
    competition_after = loadCompetition("Freebie Shark")
    competition_places_after = int(competition_after['numberOfPlaces'])
    assert available_competition_places == competition_places_after
    assert "Booking a past competition is forbidden." in response.data.decode('UTF-8')