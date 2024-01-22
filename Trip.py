from Person import Person
from Expense import Expense
from datetime import date, timedelta
from collections import defaultdict
import csv


class DateError(Exception):
    pass

class Trip(object):

    def __init__(self, start_date, length = 1) -> None:
        self.start_date = start_date #datetime.date object
        self.length = length #datetime.timedelta object
        self.end_date = None #datetime.date object
        self.total_expense = 0
        self.number_of_people = 0
        self.expenses = []
        self.trip_master = None
        self.people = {}
        self.description = None
        self.destination = None
        self.split_table = defaultdict(int)
        self.duplicate_count = defaultdict(int) # Used incase two people have identical first and last name

    def add_person(self, last_name, first_name, age = None, sex = None, id = None):
        if id is None: id = last_name + "_" + first_name + str(self.duplicate_count[last_name + "_" + first_name] + 1)
        new_person = Person(last_name, first_name, age = age, sex = sex, id = id)
        self.people.update({id:new_person})
        self.number_of_people = self.number_of_people + 1

    def set_trip_master(self, trip_master):
        self.trip_master = trip_master

    def add_expense(self, value, expense_date = None, payer = None, number_of_spliters = 1, spliters = []):
        if value < 0:
            raise ValueError("Expense must has value larger than 0")
        expense_date = date.today() if expense_date is None else date.fromisoformat(expense_date)
        if expense_date > self.end_date or expense_date < self.start_date:
            raise DateError("Expense date is not within the trip")
        if spliters and len(spliters) != number_of_spliters:
            raise ValueError("Number of spliters of this expense does not match the number of people")
        payer = self.trip_master if payer is None else payer
        new_expense = Expense(value, expense_date, payer, number_of_spliters = number_of_spliters, spliters = spliters)

    def set_date(self, start_date, end_date = None, length = None): #Input start date and end_date and/or length by str, convert them to date object
        if end_date == None and length == None: raise DateError("Please provide either trip end date or trip length")
        if end_date != None: end_date = date(end_date)
        if length != None: length = timedelta(int(length))
        start_date = date.fromisoformat(start_date)
        if end_date != None: 
            end_date = date.fromisoformat(end_date)
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
        for expense in self.expenses:
            expense_split_dict = expense.calculate_split()
            for k in expense_split_dict.keys():
                self.split_table[k] = self.split_table[k] + expense_split_dict[k]
        
        return self.split_table

    def set_description(self, description_text):
        self.description = description_text

    def add_destination(self, destination):
        self.destionation = destination

    def show_split(self):
        print(self.split_table)
           
    def save_people_to_csv(self, people_csv_path):
        with open(people_csv_path, 'w') as people_csv:
            headers = (self.people[list(self.people)[0]]).convert_to_dict.keys()
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
            headers = self.people[0].convert_to_dict.keys()
            csv_writer = csv.DictWriter(expense_csv, headers)
            csv_writer.writeheader()
            for expense in self.expenses:
                expense_dict = expense.convert_to_dict()
                csv_writer.writerow(expense_dict)

    def load_expense_from_csv(self, expense_csv_path):
        with open(expense_csv_path) as expense_csv:
            csv_reader = csv.DictReader(expense_csv)
            for expense_dict in csv_reader:
                if "date" in expense_dict:
                    expense_dict["date"] = date.fromisoformat(expense_dict["date"])
                if "spliters" in expense_dict:
                    expense_dict["spliters"] = expense_dict["spliters"].split("+")
                new_expense = Expense.from_dict(expense_dict)
                self.expenses.append(new_expense)