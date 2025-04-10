from Card import Card
from Colors import Colors
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
                    self.__deck.append(Card(int(self.__face_cards[card]), suit, f'{card} of {suit}'))
                else:
                    self.__deck.append(Card(int(card), suit, f'{card} of {suit}'))

    # Helper that shuffles the deck
    def shuffle_deck(self):
        random.shuffle(self.__deck)

    # Helper that pops off the first card of the deck
    def draw_card(self):
        drawn = False
        while not drawn:
            try:
                new_card = self.__deck.pop()
            except IndexError:
                # print("DEBUG@Deck.py@draw_card(): deck is empty, re-filling and shuffling...")
                self.create_deck()
                self.shuffle_deck()
                self.set_deck(self.get_deck())
            except BaseException as e:
                print(Colors.red+"Something went wrong while trying to draw a card, sorry!"+Colors.reset)
                print(e)
            else:
                drawn = True
        return new_card


    # Getters
    def get_deck(self):
        return self.__deck

    # Setters
    def set_deck(self, deck):
        self.__deck = deck
