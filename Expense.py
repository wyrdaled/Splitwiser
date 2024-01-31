from datetime import date

class Expense(object):

    def __init__(self, value, expense_date, payer, number_of_spliters = 1, spliters = [], location = "") -> None:
        self.value = value
        self.expense_date = expense_date
        self.payer = payer
        self.number_of_spliters = number_of_spliters
        self.spliters = spliters if spliters else [payer]
        self.category = None
        self.location = location
        self.spliters = spliters # This spliters is a list of Person object's id

    @classmethod
    def get_csv_header(cls):
        return ["value", "expense_date", "payer", "number_of_spliters", "spliters", "location"]
    
    def set_date(self, date):
        self.expense_date = date.fromisoformat(date)

    def set_payer(self, payer):
        self.payer = payer

    def set_value(self, value):
        self.value = value

    def set_spliters(self, spliters):
        self.spliters = spliters

    def add_spliters(self, spliters):
        self.spliters.extend(spliters)

    def calculate_split(self):
        #Function for actually caluclate the split, returns a dict {(debtors, payer) : value}, for now, value is always positive
        if self.number_of_spliters == 1:
            return {}
        pay_per_person = round(self.value / self.number_of_spliters, 2)
        split_dict = {(debtor, self.payer):pay_per_person for debtor in self.spliters}
        return split_dict

    def __str__(self):
        description_str = "%.2f paid by %s on %s." % (self.value, self.payer, str(self.date))
        if self.location != "":
            description_str = description_str + " Spent at %s" % self.location
        return description_str
    
    @classmethod
    def from_dict(cls, input_dict):
        new_expense = cls(input_dict["value"], input_dict["expense_date"], input_dict["payer"], input_dict["number_of_spliters"])
        for k in ["spliters", "location"]:
            if k in input_dict:
                setattr(new_expense, k, input_dict[k])
                        
        return new_expense

    def convert_to_dict(self):
        output_dict = {k:getattr(self, k) for k in ["value", "expense_date", "payer", "number_of_spliters", "spliters", "location"] if getattr(self, k, None) is not None}
        if "expense_date" in output_dict: output_dict.update({"expense_date":str(self.expense_date)}) #Change date to correct format
        if "spliters" in output_dict:
            spliter_str = '+'.join(self.spliters)
            output_dict.update({"spliters":spliter_str})

        return output_dict