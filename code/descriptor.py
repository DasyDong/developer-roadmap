# wrong_lazy_properties.py
import random
import time

class LazyProperty:
    def __init__(self, function):
        self.function = function
        self.name = function.__name__

    def __get__(self, obj, type=None) -> object:
        obj.__dict__[self.name] = self.function(obj)
        return obj.__dict__[self.name]

    def __set__(self, obj, value):
        pass

class DeepThought:
    @LazyProperty
    def meaning_of_life(self):
        time.sleep(3)
        return 42

my_deep_tought_instance = DeepThought()
print(my_deep_tought_instance.meaning_of_life)
print(my_deep_tought_instance.meaning_of_life)
print(my_deep_tought_instance.meaning_of_life)