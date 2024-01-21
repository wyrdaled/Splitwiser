#This is the py file for Person object
class Person(object):

    def __init__(self, last_name, first_name) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.age = None
        self.sex = None
        self.id = None

    def set_name(self, first_name, last_name):
        self.set_first_name(first_name)
        self.set_last_name(last_name)

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    def __str__(self):
        return self.first_name