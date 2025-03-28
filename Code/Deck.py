from Card import Card
import random


class Deck:
    __card_suits = []
    __cards_list = []
    __face_cards = {'Ace': None, 'Jack': None, 'Queen': None, 'King': None}
# - maybe default attribute values should be empty? setting dict to None then resetting it in init seems redundant
    __deck = []

    def __init__(self):
# - no setters in init???
        self.__card_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.__cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        self.__face_cards = {'Ace': 11, 'Jack': 10, 'Queen': 10, 'King': 10}
        self.__deck = []

    def create_deck(self):
# - helpers should use getters and setters(?)
# - create_deck() should be called in __init__ (?)
        for suit in self.__card_suits:
            for card in self.__cards_list:
                if card in self.__face_cards:
                    self.__deck.append(Card(int(self.__face_cards[card]), suit, f'{card} of {suit}'))
                else:
                    self.__deck.append(Card(int(card), suit, f'{card} of {suit}'))

    def shuffle_deck(self):
# - refactor to use getters+setters?
        random.shuffle(self.__deck)

    def get_deck(self):
        return self.__deck

    def draw_card(self):
        return self.__deck.pop()

    def set_deck(self, deck):
        self.__deck = deck
        return self.__deck
# - setters??? (why return in a setter???)
