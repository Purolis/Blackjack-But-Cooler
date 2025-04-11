from Card import Card
import random


class Deck:

    # Default Variables
    __card_suits = []
    __cards_list = []
    __face_cards = {}
    __deck = []

    # Initialization
    def __init__(self, deck):
        self.set_deck(deck)

    # Helper that creates the deck itself
    def create_deck(self):
        self.__card_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']
        self.__cards_list = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
        self.__face_cards = {'Ace': 11, 'Jack': 10, 'Queen': 10, 'King': 10}
        self.__deck = []

        for suit in self.__card_suits:
            for card in self.__cards_list:
                if card in self.__face_cards:
                    self.__deck.append(Card(int(self.__face_cards[card]), suit, f'{card} of {suit}', f'assets/Flat-Playing-Cards-Set/{suit}/{card[0]}.png'))
                else:
                    self.__deck.append(Card(int(card), suit, f'{card} of {suit}', f'assets/Flat-Playing-Cards-Set/{suit}/{card}.png'))

    # Helper that shuffles the deck
    def shuffle_deck(self):
        random.shuffle(self.__deck)

    # Helper that pops off the first card of the deck
    def draw_card(self):
        return self.__deck.pop()

    # Getters
    def get_deck(self):
        return self.__deck

    # Setters
    def set_deck(self, deck):
        self.__deck = deck
