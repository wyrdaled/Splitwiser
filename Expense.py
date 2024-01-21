from datetime import date

class Expense(object):

    def __init__(self, value, date, payer, number_of_spliters = 1, spliters = [], location = "") -> None:
        self.value = value
        self.date = date
        self.payer = payer
        self.number_of_spliters = number_of_spliters
        self.spliters = spliters if spliters else [payer]
        self.category = None
        self.location = location

    def set_payer(self, payer):
        self.payer = payer

    def set_value(self, value):
        self.value = value

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