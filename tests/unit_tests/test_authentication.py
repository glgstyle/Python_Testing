# // LOGIN

# test login page
def test_index_page_should_return_200(client):
    # Get login page
    response = client.get('/')
    # Check response code
    assert response.status_code == 200

# // SHOWSUMMARY


# test in all cases showSummary return status 200 or 401
def test_should_return_status_code_200_or_401(client):
    response = client.post('/showSummary', data={'email': 'blabla@gmail.com'})
    assert response.status_code == 200 or response.status_code == 401


# test good email
def test_should_return_status_200_with_good_email(client):
    response = client.post(
        '/showSummary', data={'email': 'kate@shelifts.co.uk'})
    assert response.status_code == 200


# test wrong email
def test_should_return_status_401_with_wrong_email(client):
    response = client.post('showSummary', data={'email': 'kate@shelifts.co.u'})
    assert response.status_code == 401

# // LOGOUT


# test logout
def test_logout_should_return_status_302(client):
    client.post("/showSummary", data={'email': 'kate@shelifts.co.uk'})
    response = client.get("/logout")
    assert response.status_code == 302
