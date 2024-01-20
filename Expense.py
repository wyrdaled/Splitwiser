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