class Dealer:

    # Default Variables
    __hand_value = None
    __hand = []
    __name = None

    # Initialization
    def __init__(self, hand, hand_value, name):
        self.set_hand(hand)
        self.set_hand_value(hand_value)
        self.set_name(name)

    # Draw a card function
    def draw(self, card):
        self.__hand.append(card)
        return self.__hand

    # Counts the number in the hand function
    def count_hand(self):
        self.set_hand_value(0)
        for card in self.__hand:
            self.set_hand_value(self.get_hand_value() + card.get_value())

        if self.get_hand_value() > 21:
            for card in self.get_hand():
                if card.get_value() == 11:
                    self.set_hand_value(self.get_hand_value() - 10)

        return self.get_hand_value()

    # Getters
    def get_hand(self):
        return self.__hand

    def get_hand_value(self):
        return self.__hand_value

    def get_name(self):
        return self.__name

    # Setters
    def set_hand(self, hand):
        self.__hand = hand

    def set_hand_value(self, hand_value):
        self.__hand_value = hand_value

    def set_name(self, name):
        self.__name = name

    # to_string
    def __str__(self):
        txt = ""

        # change text color to green if it is the active player, blue if not
        if self.get_name() == None:
            txt += "\033[32m" + "┌─ Your hand  🡻\n"
        else:
            txt += "\033[94m┌─ " + str(self.get_name()) + "'s hand 🡻\n"


        txt += "┝┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n"

        hand = self.get_hand()
        for i in range(len(hand)):
            txt += "├ " + str(hand[i].get_name()) + "\n"

        txt += "┝┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n"
        txt += "├─ Hand Total: " + str(self.count_hand()) + "\n"
        txt += "└───────────────────────\033[0m\n"
            # \033[0m 🡺 reset text color
        
        return txt