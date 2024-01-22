#This is the py file for Person object
import csv
class Person(object):

    def __init__(self, last_name, first_name, sex = None, age = None, id = None) -> None:
        self.last_name = last_name
        self.first_name = first_name
        self.sex = sex
        self.age = age
        if id is None:
            self.id = first_name + "_" + last_name
        
    def set_name(self, first_name, last_name):
        self.set_first_name(first_name)
        self.set_last_name(last_name)

    def set_first_name(self, first_name):
        self.first_name = first_name

    def set_last_name(self, last_name):
        self.last_name = last_name

    @classmethod
    def from_dict(cls, input_dict):
        new_person = cls.__init__(input_dict["last_name"], input_dict["first_name"])
        for k in ["sex", "age", "id"]:
            if k in input_dict:
                setattr(new_person, k, input_dict[k])
        return new_person

    def convert_to_dict(self):
        output_dict = {k:getattr(self, k) for k in ["last_name", "first_name", "sex", "age", "id"] if getattr(self, k) is not None}
        return output_dict

    def __str__(self):
        return self.first_name