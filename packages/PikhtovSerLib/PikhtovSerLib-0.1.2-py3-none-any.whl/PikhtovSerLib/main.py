from json_serealazer import JsonSerelizator
# import constants
# import math
# from inspect import getmembers
# import regex
# from constants import *
# import json
# from my_serelizator import Serelizator

class Rectangle:
    def __init__(self, a, b):
        self.a = a
        self.b = b
    @property
    def area(self):
        return self.a * self.b


d = Rectangle(4, 3)
j = JsonSerelizator()
d_s = j.dump(d, "test.json")
ds_d = j.load("test.json")
print(ds_d.area)


