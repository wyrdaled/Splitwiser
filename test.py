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
xd = nm_trip.add_person("Erdong", "Lu", sex = "male", age = 28, id='wyrda')
nm_trip.set_trip_master("wyrda")

abq_hotel = nm_trip.add_expense(413.40, "2023-11-22")
abq_hotel.set_location("Albuquerque, NM")
abq_hotel.add_spliters(["Liu_Bingqian_1","Ma_Haoyue_1","Jing_Yingze_1","Zhao_Xianyuan_1"])

print("Printing abq hotel split")
abq_hotel.show_split()
abq_hotel.set_split_mode("by_value")
abq_hotel.set_split_table({"wyrda":102.68})
abq_hotel.set_individual_split("Zhao_Xianyuan_1",62.68)
abq_hotel.show_split()
abq_hotel.set_split_mode("by_percent")
abq_hotel.set_individual_split("wyrda",0.3)
abq_hotel.set_individual_split("Ma_Haoyue_1",0.1)
abq_hotel.show_split()
#abq_hotel.set_split_table

print(nm_trip.destination)
print(nm_trip.people)
print(nm_trip)
print(os.path.abspath(os.curdir))
print(abq_hotel)

nm_trip.show_split()

nm_trip.save_trip("NM_trip")

