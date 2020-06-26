from django.shortcuts import render
from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import Flight, Passenger
from django.urls import reverse

# Create your views here.

def index(request):
    # return HttpResponse("Flights")
    
    # specific dictionary
    context = {
        "flights": Flight.objects.all()
    }
    return render(request, "flights/index.html", context)


def flight(request, flight_id):

    try:
        flight = Flight.objects.get(pk=flight_id)
    except Flight.DoesNotExist:
        raise Http404("Flight with this id doesn't exist")
    context = {
        "flight": flight,
        "passengers": flight.passengers.all(),
        "not_passengers": Passenger.objects.exclude(flights=flight).all(),
    }
    return render(request, "flights/flight.html", context)


def book(request, flight_id):

    try:
        passenger_id = int(request.POST["passenger"])
        flight = Flight.objects.get(pk=flight_id)
        passenger = Passenger.objects.get(pk=passenger_id)
    except KeyError:
        return render(request, "flights/error.html", {"error": "No flights selected"})
    except Flight.DoesNotExist:
        return render(request, "flights/error.html", {"error": "No such flights exist"})
    except Passenger.DoesNotExist:
        return render(request, "flights/error.html", {"error": "No such passenger"})
    passenger.flights.add(flight)
    return HttpResponseRedirect(reverse("flight", args=(flight_id,)))