from Person import Person
from Expense import Expense, PersonError
from datetime import date, timedelta
from collections import defaultdict
import csv
import pathlib
import os, sys
import json


class DateError(Exception):
    pass

class Trip(object):

    def __init__(self, trip_name, start_date, length = None, end_date = None, destination = None) -> None:
        self.trip_name = trip_name
        self.start_date = start_date #datetime.date object
        self.length = length #datetime.timedelta object
        self.end_date = end_date #datetime.date object
        self.total_expense = 0
        self.number_of_people = 0
        self.expenses = {}
        self.trip_master = None #Should be specified with Person.id
        self.people = {}
        self.description = None
        self.destination = destination
        self.split_table = defaultdict(int)
        self.duplicate_count = defaultdict(int) # Used incase two people have identical first and last name
        self.expense_count = defaultdict(int) #Used to give expense auto generated IDs
        self.save_path = None
        self.set_date(start_date, end_date = end_date, length = length)

    def add_person_by_obj(self, person): #Adding a person object directly, without creating the object
        self.people.update({person.id:person})
        if self.trip_master is None: self.trip_master = person.id

    def remove_person(self, people_id):
        if people_id not in self.people:
            raise PersonError("Person to be removed not in trip")
        removed_person = self.people.pop(people_id)
        self.duplicate_count[removed_person.last_name + "_" + removed_person.first_name] =\
              self.duplicate_count[removed_person.last_name + "_" + removed_person.first_name] - 1
        if self.get_number_of_people() == 0:
            self.set_trip_master(None)
        elif self.trip_master == people_id:
            self.set_trip_master(next(iter(self.people)))

    def add_person(self, last_name, first_name, age = None, sex = None, id = None, payment_method = None, acc_id = None, email = None, tel = None):
        if id is not None and id in self.people:
            print("Two people cannot have identical IDs, please specify unused ID")
        if id is None: id = self.generate_person_id(last_name, first_name)
        self.duplicate_count[last_name + "_" + first_name] = self.duplicate_count[last_name + "_" + first_name] + 1
        new_person = Person(last_name, first_name, age = age, sex = sex, id = id, payment_method = payment_method, email = email, acc_id = acc_id, tel = tel)
        self.people.update({id:new_person})
        self.number_of_people = self.number_of_people + 1
        print("TM in add person: %s" % self.trip_master)
        if self.trip_master is None: self.trip_master = id
        return new_person
    
    def generate_person_id(self, last_name, first_name):
        return last_name + "_" + first_name + "_" + str(self.duplicate_count[last_name + "_" + first_name] + 1)

    def set_trip_master(self, trip_master):
        if trip_master is not None and trip_master not in self.people:
            raise PersonError("Person %s is not in this trip")
        self.trip_master = trip_master #trip master should be person's id

    def get_number_of_people(self):
        return len(self.people)

    def add_expense(self, value, expense_date = None, payer = None, number_of_spliters = 1, spliters = [], id = None):
        if value < 0:
            raise ValueError("Expense must has value larger than 0")
        expense_date = date.today() if expense_date is None else date.fromisoformat(expense_date)
        if expense_date > self.end_date or expense_date < self.start_date:
            raise DateError("Expense date is not within the trip")
        if spliters and len(spliters) != number_of_spliters:
            raise ValueError("Number of spliters of this expense does not match the number of people")
        for spliter in spliters:
            if spliter not in self.people:
                raise PersonError("Unrecognized person id: %s" % spliter)
        if id is None:
            id = str(expense_date) + "_" + str(self.expense_count[str(expense_date)] + 1)
        payer = self.trip_master if payer is None else payer
        if payer not in self.people:
            raise PersonError("Payer %s is not a person in this trip" % payer)
        new_expense = Expense(value, expense_date, payer, number_of_spliters = number_of_spliters, spliters = spliters, id = id, trip = self)
        self.expenses.update({new_expense.id:new_expense})
        return new_expense

    def set_date(self, start_date, end_date = None, length = None): #Input start date and end_date and/or length by str, convert them to date object
        if end_date == None and length == None: raise DateError("Please provide either trip end date or trip length")
        #if end_date != None: end_date = date.fromisoformat(end_date)
        if length != None: length = timedelta(int(length))
        start_date = date.fromisoformat(start_date) if isinstance(start_date, str) else start_date
        if end_date != None: 
            end_date = date.fromisoformat(end_date) if isinstance(end_date, str) else end_date
            if end_date < start_date: raise DateError("End date is earlier than start date")
            date_delta = end_date - start_date
            if date_delta.days > 365: raise DateError("Trip longer than 1 year is not supported")
            if length != None and length != date_delta: raise DateError("Length and start / end date mismatch")
            length = date_delta
            
        if length != None:
            if length.days < 1: raise DateError("Trip length cannot be short than 1 day")
            end_date = start_date + length

        self.start_date = start_date
        self.end_date = end_date
        self.length = length

    def calculate_trip_split(self):
        for expense in self.expenses.values():
            expense_split_dict = expense.calculate_split()
            for k in expense_split_dict.keys():
                self.split_table[k] = self.split_table[k] + expense_split_dict[k]
        
        return self.split_table

    def set_description(self, description_text):
        self.description = description_text

    def add_destination(self, destination):
        self.destination = destination

    def show_split(self):
        self.calculate_trip_split()
        print(self.split_table)
           
    def save_people_to_csv(self, people_csv_path):
        with open(people_csv_path, 'w') as people_csv:
            headers = Person.get_csv_header()
            csv_writer = csv.DictWriter(people_csv, headers)
            csv_writer.writeheader()
            for person_id in self.people:
                person_dict = self.people[person_id].convert_to_dict()
                csv_writer.writerow(person_dict)

    def load_people_from_csv(self, people_csv_path):
        with open(people_csv_path) as people_csv:
            csv_reader = csv.DictReader(people_csv)
            for person_dict in csv_reader:
                new_person = Person.from_dict(person_dict)
                self.people.update({new_person.id:new_person})

    def save_expense_to_csv(self, expense_csv_path):
        with open(expense_csv_path, 'w') as expense_csv:
            headers = Expense.get_csv_header()
            csv_writer = csv.DictWriter(expense_csv, headers)
            csv_writer.writeheader()
            for expense_id in self.expenses:
                expense_dict = self.expenses[expense_id].convert_to_dict()
                csv_writer.writerow(expense_dict)

    def load_expense_from_csv(self, expense_csv_path):
        with open(expense_csv_path) as expense_csv:
            csv_reader = csv.DictReader(expense_csv)
            for expense_dict in csv_reader:
                if "date" in expense_dict:
                    expense_dict["expense_date"] = date.fromisoformat(expense_dict["date"])
                if "spliters" in expense_dict:
                    expense_dict["spliters"] = expense_dict["spliters"].split("+")
                new_expense = Expense.from_dict(expense_dict)
                new_expense.trip = self
                self.expenses.update({new_expense.id:new_expense})

    def save_trip(self, trip_path = None):
        if trip_path is None: trip_path = str(self)
        trip_path = os.path.abspath(trip_path)
        trip_path = pathlib.Path(trip_path)
        trip_path.mkdir(exist_ok=True)
        people_csv_path = os.path.join(trip_path, "people.csv")
        expense_csv_path = os.path.join(trip_path, "expense.csv")
        info_dict = {k: getattr(self, k) for k in \
                     ["trip_name", "start_date", "end_date", "length", "total_expense", "number_of_people", "trip_master",\
                      "description", "destination", "splite_table", "duplicate_count", "expense_count"] \
                     if getattr(self, k, None) is not None}
        if "start_date" in info_dict: info_dict["start_date"] = str(info_dict["start_date"])
        if "end_date" in info_dict: info_dict["end_date"] = str(info_dict["end_date"])
        if "length" in info_dict: info_dict["length"] = info_dict["length"].days
        info_dict_path = os.path.join(trip_path, "info_dict.json")
        with open(info_dict_path, "w") as info_dict_file:
            json.dump(info_dict, info_dict_file)
        self.save_people_to_csv(people_csv_path)
        self.save_expense_to_csv(expense_csv_path)
        self.trip_path = os.path.abspath(trip_path)
    
    @classmethod
    def load_trip(cls, trip_path):
        trip_path = os.path.abspath(trip_path)
        if not os.path.isdir(trip_path):
            raise FileNotFoundError("Invalid trip - directory not exist, loading failed.")
        if not os.path.isfile(os.path.join(trip_path, "info_dict.json")):
            raise FileNotFoundError("Invalid trip - file missing, loading failed.")
        with open(os.path.join(trip_path, "info_dict.json")) as info_dict_file:
            info_dict = json.load(info_dict_file)
        start_date = date.fromisoformat(info_dict["start_date"])
        end_date = date.fromisoformat(info_dict["end_date"]) if info_dict["end_date"] else (start_date + timedelta(info_dict["length"]))
        new_trip = cls(start_date, end_date = end_date)
        new_trip.length = (end_date - start_date).days
        for attr in ["total_expense", "number_of_people", "trip_master", "description", "destination", "splite_table", "duplicate_count", "expense_count"]:
            if attr in info_dict: setattr(new_trip, attr, info_dict[attr])
        people_csv_path = os.path.join(trip_path, "people.csv")
        expense_csv_path = os.path.join(trip_path, "expense.csv")
        new_trip.load_expense_from_csv(expense_csv_path)
        new_trip.load_people_from_csv(people_csv_path)
        new_trip.save_path = os.path.abspath(trip_path)
        return new_trip
        
    def __str__(self):
        start_date_str = str(self.start_date)
        end_date_str = str(self.end_date)
        ret_str = start_date_str + " to " + end_date_str + " trip"
        if self.destination: ret_str = ret_str + " to " + self.destination
        if self.number_of_people: ret_str = ret_str + " for " + str(self.number_of_people) + " people"
        ret_str = self.trip_name + ": " + ret_str
        return ret_str
    