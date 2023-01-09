import pytest
from server import app as app_flask


# create a test web browser
@pytest.fixture
def client():
    app = app_flask
    with app.test_client() as client:
        yield client
