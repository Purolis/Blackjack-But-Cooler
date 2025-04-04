from Dealer import Dealer


class Player(Dealer):

    # Default Variables
    __player_wealth = None
    __items = {}

    # Initialization
    def __init__(self, hand, hand_value, wealth, items):
        super().__init__(hand, hand_value)
        self.set_player_wealth(wealth)
        self.set_items(items)

    # helpers
    def print_item(self, item):
        print(f'You sold your {item}! You got ${self.get_value(item)} for it!')
        self.set_player_wealth(self.__items.pop(item))

    # Getters
    def get_player_wealth(self):
        return self.__player_wealth

        def get_items(self):
        return self.__items

    def get_value(self, item):
        return self.__items.get(item)

    def get_all_items(self):
        return len(self.__items)

    # Setters
    def set_player_wealth(self, player_wealth):
        self.__player_wealth = player_wealth

    def set_items(self, items):
        self.__items = items
