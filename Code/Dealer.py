from Colors import Colors

class Dealer:

    # Default Variables
    __hand_value = None
    __hand = []
    __name = None
    __flags = {} # boolean flags to determine game state

    # Initialization
    def __init__(self, hand, hand_value, name):
        self.set_hand(hand)
        self.set_hand_value(hand_value)
        self.set_name(name)
        self.set_all_flags({
            "bust": False,
            "natural_blackjack": False,
            "blackjack": False,
            "push": False,
            "hide_hole": False,
            "finished_turn": False,
        })

    # Helpers
    def draw(self, card):
        if self.get_flags()["bust"]:
            print("DEBUG@Dealer.py@draw(): client is busted, no drawing")
        else:
            self.__hand.append(card)

    def count_hand(self):
        # Counts the total value of all cards in the hand
        # print("DEBUG@Dealer.py@count_hand()")
        self.set_hand_value(0)
        new_value = 0
        for card in self.get_hand():
            new_value += int(card.get_value())

        i = -1
        hand = self.get_hand()
        while (new_value > 21) and (i < (len(hand)-1)):
            i += 1
            if hand[i].get_value() == 11: # try to count Ace as 1 instead of 10 if you might bust
                new_value -= 10

        self.set_hand_value(new_value)

    def reset_flags(self):
        for flag in self.get_flags():
            self.set_flag(flag, False)
        # print("DEBUG@Dealer.py@reset_flags() flags reset")

    # Getters
    def get_hand(self):
        return self.__hand

    def get_hand_value(self):
        # print("DEBUG@Dealer.py@get_hand_value()")
        self.count_hand()
        return self.__hand_value

    def get_name(self):
        return self.__name

    def get_flags(self):
        return self.__flags

    # Setters
    def set_hand(self, hand):
        self.__hand = hand

    def set_hand_value(self, hand_value):
        self.__hand_value = hand_value

    def set_name(self, name):
        self.__name = name

    def set_flag(self, flag, state):
        self.__flags[flag] = state

    def set_all_flags(self, flags):
        self.__flags = flags

    # to_string
    def __str__(self):
        txt = ""
        flags = self.get_flags()
        color = None

        # change text color to green if it is the active player, blue if not, and yellow if dealer
        if self.get_name() == None:
            color = Colors.green
            txt += color + "╒═══════════════════════\n├─ "+Colors.white+"Your"+color+" hand  🡻\n"
        elif self.get_name() == "DEALER":
            color = Colors.orange
            txt += color + "╒═══════════════════════\n├─ " +Colors.white+ str(self.get_name()).lower() +color+ "'s hand 🡻\n"
        else:
            color = Colors.blue
            txt += color + "╒═══════════════════════\n├─ " +Colors.white+ str(self.get_name()).lower() +color+ "'s hand 🡻\n"

        txt += "┝┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n"

        hand = self.get_hand()

        flag_msg = "" # message to display conditionally
        if flags["bust"]:
            flag_msg += "├─ "+Colors.red+"BUSTED"+color+"\n"
        elif flags["blackjack"]:
            flag_msg += "├─ "+Colors.yellow+"BLACKJACK"+color+"\n"
        elif flags["natural_blackjack"]:
            flag_msg += "├─ "+Colors.yellow+"NATURAL BLACKJACK"+color+"\n"
        elif flags["push"]:
            flag_msg += "├─ "+Colors.yellow+"PUSH"+color+"\n"

        if flags["hide_hole"]:
            # if dealer, hide all but one card (hide hole card(s))
            txt += "├ " + str(hand[0].get_card_name()) + "\n"
            txt += "├ [hidden] \n"
            txt += "┝┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n"
            txt += "├─ Shown Hand Total: " + str(hand[0].get_value()) + "\n"
            txt += "╘═══════════════════════"+Colors.reset
            return txt
        else:
            for i in range(len(hand)):
                txt += "├ " + str(hand[i].get_card_name()) + "\n"
            txt += "┝┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅┅\n"
            txt += "├─ Hand Total: " + str(self.get_hand_value()) + "\n"
            txt += flag_msg
            txt += "╘═══════════════════════"+Colors.reset
        
        return txt