from Dealer import Dealer


class Player(Dealer):

    # Default Variables
    __hand_value = None
    __hand = []
    __player_wealth = None

    # Initialization
    def __init__(self, hand, hand_value, wealth):
        super().__init__(hand, hand_value)
        self.set_player_wealth(wealth)

    # Getters
    def get_player_wealth(self):
        return self.__player_wealth

    # Setters
    def set_player_wealth(self, player_wealth):
        self.__player_wealth = player_wealth
