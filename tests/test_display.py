from .utils import loadClubs
# They should be able to see the list of clubs and their associated current points balance


def test_should_display_list_of_clubs(client):
    """Test if the list of clubs well displayed on page."""
    response= client.get('/pointsDisplayBoard')
    clubs = loadClubs()
    for club in clubs:
        name = club['name']
        points = club['points']
        expecting_data = "<li>\n            "+ name + "<br />\n            " + "Points: " + points + "</br>\n        </li>\n"
        assert expecting_data in response.data.decode('UTF-8')
    assert response.status_code == 200