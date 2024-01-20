from Person import Person
from Expense import Expense
from datetime import date


class DateError(Exception):
    pass

class Trip(object):

    def __init__(self, start_date, length = 1) -> None:
        self.start_date = start_date
        self.length = length
        self.end_date = None
        self.total_expense = 0
        self.number_of_people = 0
        self.expenses = []
        self.trip_master = None
        self.people = []
        self.description = None
        self.destination = None

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

    def set_date(self, start_date, end_date = None, length = None):
        if end_date == None and length == None: raise DateError("Please provide either trip end date or trip length")
        #TODO - implement max date length check
        #TODO - implement date diff == length check
        self.start_date = start_date
        if end_date != None:
            self.end_date = end_date
            #TODO: calculate length
        if length != None:
            self.length = length
            #TODO: calculate end_date

    def set_description(self, description_text):
        self.description = description_text

    def add_destination(self, destination):
        self.destionation = destination

           
