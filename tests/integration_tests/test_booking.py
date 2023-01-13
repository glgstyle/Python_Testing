from ..utils import reset_data
import pytest


# book with sufficient points balance
@pytest.mark.integtest
def test_sufficient_points_balance_should_return_status_200(client):
    """
    Test club book a competition with sufficient points balance.
    """
    reset_data()
    response = client.post('/purchasePlaces', data={
      "club": "She Lifts",
      "competition": "Spring Festival",
      "places": 12
    })
    assert response.status_code == 200
