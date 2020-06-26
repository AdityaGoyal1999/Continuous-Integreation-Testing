from django.test import TestCase, Client
from django.db.models import Max

from .models import Flight, Airport, Passenger
# Create your tests here.

class ModelsTestCase(TestCase):

    # A must function for this class. It is run before every function
    def setUp(self):

        # create airports

        # Only Creates the object and DOESN'T save it
        # a1 = Airport(code="JFK", city="New York")
        # a2 = Airport(code="LHR", city="London")

        # Save the object with creation
        a1 = Airport.objects.create(code="JFK", city="New York")
        a2 = Airport.objects.create(code="LHR", city="London")

        # create Flight

        Flight.objects.create(origin=a1, destination=a2, duration=5000)
        Flight.objects.create(origin=a1, destination=a1, duration=5000)
        Flight.objects.create(origin=a1, destination=a2, duration=-100)

    def test_departure_count(self):
        a = Airport.objects.get(code="JFK")
        self.assertEqual(a.departures.count(), 3)

    def test_arrivals_count(self):
        a = Airport.objects.get(code="JFK")
        self.assertEqual(a.arrivals.count(), 1)

    def test_valid_flight(self):
        a1 = Airport.objects.get(code="JFK")
        a2 = Airport.objects.get(code="LHR")
        f = Flight.objects.get(origin=a1, destination=a2, duration="5000")
        self.assertTrue(f.is_valid())

    def test_invalid_flight_airport(self):
        a1 = Airport.objects.get(code="JFK")
        f = Flight.objects.get(origin=a1, destination=a1)
        self.assertFalse(f.is_valid())

    def test_invalid_flight_duration(self):
        # a1 = Airport.objects.get(code="JFK")
        # a2 = Airport.objects.get(code="LHR")
        f = Flight.objects.get(duration=-100)
        self.assertFalse(f.is_valid())

    def test_index(self):
        c = Client()
        response = c.get("/")
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(response)
        self.assertEqual(response.context["flights"].count(), 3)

    def test_valid_flight(self):

        a1 = Airport.objects.get(code="JFK")
        f = Flight.objects.get(destination=a1)

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)

    def test_invalid_flight_page(self):
        
        max_id = Flight.objects.all().aggregate(Max("id"))["id__max"]
        a1 = Airport.objects.get(code="JFK")
        f = Flight.objects.get(destination=a1)
        c = Client()
        response = c.get(f"/{f.id + 5}")
        self.assertEqual(response.status_code, 404)

    def test_flight_page_passengers(self):

        a1 = Airport.objects.get(code="JFK")
        f = Flight.objects.get(destination=a1)
        p = Passenger.objects.create(first="Aditya", last="Goyal")
        p.flights.add(f)

        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["passengers"].count(), 1)

    def test_flight_page_not_passengers(self):

        a1 = Airport.objects.get(code="JFK")
        f = Flight.objects.get(destination=a1)
        c = Client()
        response = c.get(f"/{f.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["not_passengers"].count(), 0)