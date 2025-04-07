class Player:
    __hand_value = None
    __hand = []
    __wealth = -1
    __items = {}

    def __init__(self, hand, hand_value, wealth, items):
        self.set_hand(hand)
        self.set_hand_value(hand_value)
        self.set_player_wealth(wealth)
        self.set_items(items)

        # money should be a player attribute.

    def draw(self, card):
        self.__hand.append(card)
        return self.__hand

    def count_hand(self):
        self.__hand_value = 0
        for card in self.__hand:
            self.__hand_value += card.get_value()

        if self.__hand_value > 21:
            for card in self.__hand:
                if card.get_value() == 11:
                    self.__hand_value -= 10

        return self.__hand_value

    def print_item(self, item):
        print(f'You sold your {item}! You got ${self.get_value(item)} for it!')
        self.set_player_wealth(self.__items.pop(item))

    def get_hand(self):
        return self.__hand

    def get_hand_value(self):
        return self.__hand_value

    def get_player_wealth(self):
        return self.__player_wealth

    def get_items(self):
        return self.__items

    def get_value(self, item):
        return self.__items.get(item)

    def get_all_items(self):
        return len(self.__items)

    def set_hand(self, hand):
        self.__hand = hand

    def set_hand_value(self, hand_value):
        self.__hand_value = hand_value

    def set_player_wealth(self, cash):
        self.__player_wealth = cash

    def set_items(self, items):
        self.__items = items
