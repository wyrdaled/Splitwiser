from Person import Person
from Expense import Expense
from datetime import date, timedelta
from collections import defaultdict


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
        self.people = []
        self.description = None
        self.destination = None
        self.split_table = defaultdict(int)

    def add_person(self, last_name, first_name, age = None, sex = None):
        new_person = Person(last_name, first_name, age = age, sex = sex, id = self.number_of_people)
        self.people.append(new_person)
        self.number_of_people = self.number_of_people + 1

    def set_trip_master(self, trip_master):
        self.trip_master = trip_master

    def add_expense(self, value, expense_date = None, payer = None, number_of_spliters = 1, spliters = []):
        if value > 0:
            raise ValueError("Expense must has value larger than 0")
        #TODO: check epsense_date to be in between start and end date
        expense_date = date.today() if expense_date is None else expense_date
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
           
