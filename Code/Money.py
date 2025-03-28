class Money:
    __player_wealth = None

    def __init__(self, player):
        self.__player_wealth = player

    def get_player_wealth(self):
        return self.__player_wealth

    def set_player_wealth(self, cash):
        self.__player_wealth = cash
