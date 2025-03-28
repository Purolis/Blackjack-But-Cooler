


class Money:

    def __init__(self, player, computer):

        self._playerWealth = player
        self._computerWealth = computer

    def get_playerWealth(self):
        return self._playerWealth

    def get_computerWealth(self):
        return self._playerWealth

    def set_playerWealth(self, cash):
        self._playerWealth = cash

    def set_computerWealth(self, cash):
        self._computerWealth = cash
