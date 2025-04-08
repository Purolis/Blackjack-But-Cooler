from Deck import Deck
from Player import Player
from Dealer import Dealer
import os
import time

# testing to make sure my changes work and don't cause a Chernobyl-esque disaster
# this highlights the changes I made

decklist = Deck([])
decklist.create_deck()
decklist.shuffle_deck()

starting_items = {
	"House": 170_000,
	"Car": 25_000,
	"Shoes": 90,
	"The shirt off your back": 10,
	"Dog": 9999999999999999999999999,
}

d1 = Dealer([],0,"Dealer")
p1 = Player([],0,"Your",0,{})

d1.draw(decklist.draw_card())
d1.draw(decklist.draw_card())
d1.draw(decklist.draw_card())
d1.draw(decklist.draw_card())

p1.draw(decklist.draw_card())
p1.draw(decklist.draw_card())



print(d1)
print(p1)