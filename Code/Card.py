class Card:

    # Default Variables
    __value = None
    __suit = None
    __name = None

    # Initialization
    def __init__(self, value, suit, name):
        self.set_value(value)
        self.set_suit(suit)
        self.set_name(name)

    # Getters
    def get_value(self):
        return self.__value

    def get_suit(self):
        return self.__suit

    def get_name(self):
        return self.__name

    # Setters
    def set_value(self, value):
        self.__value = value
        return self.__value

    def set_suit(self, suit):
        self.__suit = suit
        return self.__suit

    def set_name(self, name):
        self.__name = name
        return self.__name
