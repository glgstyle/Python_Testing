from locust import HttpUser, task
# from ..utils import reset_data

class ProjectPerfTest(HttpUser):
    def on_start(self):
        self.client.post('/showSummary', {
            'email':'kate@shelifts.co.uk'
        })


    @task
    def index(self):
        self.client.get('/')


    @task
    def purchase_places(self):
        # reset_data()
        self.client.post('/purchasePlaces', {
        "club": "She Lifts",
        "competition": "Spring Festival",
        "places": 12
        })


    @task
    def points_display_board(self):
        self.client.get('/pointsDisplayBoard')


    @task
    def book_a_competition(self):
        self.client.get('/book/<competition>/<club>')


    @task
    def logout(self):
        self.client.get('/logout')
