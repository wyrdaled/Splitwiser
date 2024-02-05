from datetime import date
from collections import defaultdict

class PersonError(Exception):
    pass

class Expense(object):

    def __init__(self, value, expense_date, payer, number_of_spliters = 1, spliters = [], location = "", id = None, trip = None) -> None:
        self.value = value
        self.expense_date = expense_date
        self.payer = payer
        self.number_of_spliters = number_of_spliters
        self.spliters = spliters if spliters != [] else [payer]
        self.category = None
        self.location = location
        self.id = id
        self.trip = trip

    @classmethod
    def get_csv_header(cls):
        return ["value", "expense_date", "payer", "number_of_spliters", "spliters", "location", "id"]
    
    def set_date(self, date):
        self.expense_date = date.fromisoformat(date)

    def set_payer(self, payer):
        if payer not in self.trip.people:
            raise PersonError("Payer %s is not a person in this trip")
        self.payer = payer
        if payer not in self.spliters:
            self.spliters.append(payer)

    def set_value(self, value):
        self.value = value

    def set_spliters(self, spliters):
        if self.spliters == []:
            raise PersonError("There must be at least one spliter")
        self.validate_spliters(spliters)
        self.spliters = spliters
        if self.payer not in self.spliters: #If payer has been removed from the spliteres list, then assign the first person to be payer
            print("Auto assign new payer to be %s" % self.spliters[0])
            self.payer = self.spliters[0]
        self.number_of_spliters = len(self.spliters)

    def add_spliters(self, spliters):
        self.validate_spliters(spliters)
        self.spliters.extend(spliters)
        self.number_of_spliters = len(self.spliters)

    def remove_spliters(self, spliters):
        if len(self.spliters) <= len(spliters):
            raise PersonError("Cannot remove spliters - there must be at least one person remaining")
        self.validate_spliters(spliters)
        for spliter in spliters:
            self.spliters.remove(spliter)
        if self.payer not in self.spliters: #If payer has been removed from the spliteres list, then assign the first person to be payer
            print("Auto assign new payer to be %s" % self.spliters[0])
            self.payer = self.spliters[0]
        self.number_of_spliters = len(self.spliters)

    def set_location(self, location):
        self.location = location

    def validate_spliters(self, spliters):
        if not isinstance(spliters, list):
            raise TypeError("Spliters must be a list")
        for spliter in spliters:
            if spliter not in self.trip.people:
                raise PersonError("%s is not a person in this trip" % spliter)

    def calculate_split(self):
        #Function for actually caluclate the split, returns a dict {(debtors, payer) : value}, for now, value is always positive
        if self.number_of_spliters == 1:
            return {}
        pay_per_person = round(self.value / self.number_of_spliters, 2)
        split_dict = {(debtor, self.payer):pay_per_person for debtor in self.spliters}
        return split_dict

    def __str__(self):
        description_str = "%.2f paid by %s on %s." % (self.value, self.payer, str(self.expense_date))
        if self.location != "":
            description_str = description_str + " Spent at %s" % self.location
        return description_str
    
    @classmethod
    def from_dict(cls, input_dict):
        new_expense = cls(input_dict["value"], input_dict["expense_date"], input_dict["payer"], input_dict["number_of_spliters"], id = input_dict["id"])
        for k in ["spliters", "location"]:
            if k in input_dict:
                setattr(new_expense, k, input_dict[k])
        if getattr(new_expense, "value", None) is not None:
            setattr(new_expense, "value", float(getattr(new_expense, "value")))
        if getattr(new_expense, "number_of_spliters", None) is not None:
            setattr(new_expense, "number_of_spliters", int(getattr(new_expense, "number_of_spliters")))
        if isinstance(new_expense.spliters, str):
            new_expense.spliters = new_expense.spliters.split("+")
                        
        return new_expense

    def convert_to_dict(self):
        output_dict = {k:getattr(self, k) for k in Expense.get_csv_header() if getattr(self, k, None) is not None}
        if "expense_date" in output_dict: output_dict.update({"expense_date":str(self.expense_date)}) #Change date to correct format
        if "spliters" in output_dict:
            spliter_str = '+'.join(self.spliters)
            output_dict.update({"spliters":spliter_str})

        return output_dict