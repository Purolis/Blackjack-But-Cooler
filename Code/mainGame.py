


class Money:

    def __init__(self):

        self._playerWealth = 100
        self._computerWealth = 200

    def get_playerWealth(self):
        return self._playerWealth

    def get_computerWealth(self):
        return self._playerWealth

    def set_playerWealth(self, cash):
        self._playerWealth = cash

    def set_computerWealth(self, cash):
        self._computerWealth = cash
