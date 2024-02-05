from Trip import Trip
import os, sys

new_trip = Trip.load_trip("NM_trip")
print(new_trip)
print(new_trip.people)
print(new_trip.expenses)
new_trip.show_split()