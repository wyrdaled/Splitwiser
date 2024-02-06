from datetime import date
from collections import defaultdict

class PersonError(Exception):
    pass

class ExpenseError(Exception):
    pass

class Expense(object):

    def __init__(self, value, expense_date, payer, number_of_spliters = 1, spliters = [], \
                 location = "", id = None, trip = None, split_mode = "even", split_table={}) -> None:
        self.value = value
        self.expense_date = expense_date
        self.payer = payer
        self.number_of_spliters = number_of_spliters
        self.spliters = spliters if spliters != [] else [payer]
        self.category = None
        self.location = location
        self.id = id
        self.split_mode = split_mode
        self.trip = trip
        self.split_table = split_table

    @classmethod
    def get_csv_header(cls):
        return ["value", "expense_date", "payer", "number_of_spliters", "spliters", "location", "id", "split_mode", "split_table"]
    
    def set_date(self, date):
        self.expense_date = date.fromisoformat(date)

    def set_location(self, location):
        self.location = location

    def set_payer(self, payer):
        if payer not in self.trip.people:
            raise PersonError("Payer %s is not a person in this trip")
        self.payer = payer
        if payer not in self.spliters:
            print("Adding payer %s to spliters" % payer)
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
 
    def validate_spliters(self, spliters):
        if not isinstance(spliters, list):
            raise TypeError("Spliters must be a list")
        for spliter in spliters:
            if spliter not in self.trip.people:
                raise PersonError("%s is not a person in this trip" % spliter)

    def set_split_mode(self, mode):
        if mode not in ("even", "by_percent", "by_value"):
            raise ValueError("Mode must be even, by_percent, or by_value")
        self.split_table = {}
        self.split_mode = mode

    def reset_split(self):
        self.split_table = {}
        self.split_mode = "even"

    def set_split_table(self, split_table):
        self.split_table = split_table
    
    def set_individual_split(self, person, split_value):
        self.split_table.update({person:split_value})

    def validate_split_table(self):
        if self.split_table == {}: #If split_table is empty, then it must be even split
            self.split_mode = "even"
            return

        for person in self.split_table:
            if person not in self.spliters:
                raise PersonError("Spliter table contains people not in list of spliters")
            
        if self.split_mode == "by_value":
            total_value = 0
            for expense_value in self.split_table.values():
                total_value = total_value + expense_value
            if total_value > self.value:
                raise ExpenseError("Sum of specified split values is large than expense value")
        
        elif self.split_mode == "by_percent":
            total_percent = 0
            for expense_percent in self.split_table.values():
                total_percent = total_percent + expense_percent
            if total_percent > 1:
                raise ExpenseError("Sum of specified split percentiles is larger than 1")
            
        elif self.split_mode == "even":
            return

        else:
            raise ExpenseError("Unknown split mode.\n Split mode should be even, by value, or by percent")

    def calculate_split(self):
        #split_dict is the returned result; split_table is the specified input uneven split
        #Function for actually caluclate the split, returns a dict {(debtors, payer) : value}, for now, value is always positive
        if self.number_of_spliters == 1:
            return {}
        
        self.validate_split_table()

        if self.split_mode == "even":
            pay_per_person = round(self.value / self.number_of_spliters, 2)
            split_dict = {(debtor, self.payer):pay_per_person for debtor in self.spliters}

        elif self.split_mode == "by_value":
            split_dict = {}
            current_total_value = 0
            self.validate_split_table()
            for debtor, split_value in self.split_table.items(): #First calculate people with specified split
                split_dict.update({(debtor, self.payer):split_value})
                current_total_value = current_total_value + split_value
            unspecified_people_count = self.number_of_spliters - len(self.split_table)
            pay_per_person = round((self.value-current_total_value) / unspecified_people_count, 2)
            for debtor in self.spliters: #Then calculate people with no specified split
                if debtor not in self.split_table:
                    split_dict.update({(debtor, self.payer):pay_per_person})

        elif self.split_mode == "by_percent":
            split_dict = {}
            current_total_percent = 0
            self.validate_split_table()
            for debtor, split_percent in self.split_table.items(): #First calculate people with specified split
                split_dict.update({(debtor, self.payer):split_percent})
                current_total_percent = current_total_percent + split_percent
            unspecified_people_count = self.number_of_spliters - len(self.split_table)
            percent_per_person = round((1-current_total_percent) / unspecified_people_count, 2)
            for debtor in self.spliters: #Then calculate people with no specified split
                if debtor not in self.split_table:
                    split_dict.update({(debtor, self.payer):percent_per_person})
            for k, percent in split_dict.items():
                split_dict.update({k:round(self.value * percent, 2)}) #Convert percent to value

        return split_dict

    def __str__(self):
        description_str = "%.2f paid by %s on %s." % (self.value, self.payer, str(self.expense_date))
        if self.location != "":
            description_str = description_str + " Spent at %s" % self.location
        return description_str
    
    @classmethod
    def from_dict(cls, input_dict):
        new_expense = cls(input_dict["value"], input_dict["expense_date"], input_dict["payer"], input_dict["number_of_spliters"],\
                          id = input_dict["id"], split_mode = input_dict["split_mode"])
        for k in ["spliters", "location", "split_table"]:
            if k in input_dict:
                setattr(new_expense, k, input_dict[k])
        if getattr(new_expense, "value", None) is not None:
            setattr(new_expense, "value", float(getattr(new_expense, "value")))
        if getattr(new_expense, "number_of_spliters", None) is not None:
            setattr(new_expense, "number_of_spliters", int(getattr(new_expense, "number_of_spliters")))
        if getattr(new_expense, "split_table", None) is not None:
            setattr(new_expense, "split_table", eval(getattr(new_expense, "split_table")))
        if isinstance(new_expense.spliters, str):
            new_expense.spliters = new_expense.spliters.split("+")
                        
        return new_expense

    def convert_to_dict(self):
        output_dict = {k:getattr(self, k) for k in Expense.get_csv_header() if getattr(self, k, None) is not None}
        if "expense_date" in output_dict: output_dict.update({"expense_date":str(self.expense_date)}) #Change date to correct format
        if "split_table" in output_dict: output_dict.update({"split_table":str(self.split_table)})
        if "spliters" in output_dict:
            spliter_str = '+'.join(self.spliters)
            output_dict.update({"spliters":spliter_str})

        return output_dict
    
    def show_split(self): #debug output function
        split_dict = self.calculate_split()
        print(split_dict)