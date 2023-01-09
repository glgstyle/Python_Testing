import pytest
from server import app as app_flask


@pytest.fixture
def client():
    app = app_flask
    with app.test_client() as client:
        yield client

