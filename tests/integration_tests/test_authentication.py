import pytest


# // LOGIN

# test login page
@pytest.mark.integtest
def test_index_page_should_return_200(client):
    # Get login page
    response = client.get('/')
    # Check response code
    assert response.status_code == 200


# test good email
@pytest.mark.integtest
def test_should_return_status_200_with_good_email(client):
    response = client.post(
        '/showSummary', data={'email': 'kate@shelifts.co.uk'})
    assert response.status_code == 200


# // LOGOUT

# test logout
@pytest.mark.integtest
def test_logout_should_return_status_302(client):
    client.post("/showSummary", data={'email': 'kate@shelifts.co.uk'})
    response = client.get("/logout")
    assert response.status_code == 302
