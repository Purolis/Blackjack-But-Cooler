class Card:
    __value = None
    __suit = None
    __name = None

    def __init__(self, value, suit, name):
# - init does not use setters
        self.__value = value
        self.__suit = suit
        self.__name = name

    def get_value(self):
        return self.__value

    def get_suit(self):
        return self.__suit

    def get_name(self):
        return self.__name

    def set_value(self, value):
        self.__value = value
        return self.__value
# - returning in setter?

    def set_suit(self, suit):
        self.__suit = suit
        return self.__suit
# - returning in setter?

    def set_name(self, name):
        self.__name = name
        return self.__name
# - returning in setter?
# also __str__ functions are absent from Classes
# 
