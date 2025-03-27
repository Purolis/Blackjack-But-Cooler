class Dealer:
    def __init__(self):
        self.__hand_value = 0
        self.__hand = []

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
                    break

        return self.__hand_value

    def get_hand(self):
        return self.__hand

    def get_hand_value(self):
        return self.__hand_value