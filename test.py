#This is the test driver code
from Trip import Trip
from Person import Person
import os, sys

nm_trip = Trip("2023-11-22", end_date = "2023-11-27")
nm_trip.add_destination("New Mexico")
bq = nm_trip.add_person("Liu", "Bingqian", sex = "female")
hy = nm_trip.add_person("Ma", "Haoyue", sex = "female")
jc = nm_trip.add_person("Jing", "Yingze", sex = "male")
xy = nm_trip.add_person("Zhao", "Xianyuan", sex = "male")
xd = nm_trip.add_person("Erdong", "Lu", sex = "male", age = 28)



nm_trip.add_expense(413.40, "2023-11-22", "Erdong_Lu1")

print(nm_trip.destination)
print(nm_trip.people)
print(nm_trip)
print(os.path.abspath(os.curdir))
nm_trip.save_trip("NM_trip")

