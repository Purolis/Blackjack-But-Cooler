class Player:
    __hand_value = None
    __hand = []
    __wealth = 1000

    def __init__(self, hand, hand_value, wealth):
        self.set_hand(hand)
        self.set_hand_value(hand_value)
        self.set_player_wealth(wealth)
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

    def get_hand(self):
        return self.__hand

    def get_hand_value(self):
        return self.__hand_value

    def get_player_wealth(self):
        return self._player_wealth

    def set_hand(self, hand):
        self.__hand = hand

    def set_hand_value(self, hand_value):
        self.__hand_value = hand_value

    def set_player_wealth(self, cash):
        self._player_wealth = cash
