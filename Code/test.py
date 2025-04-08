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
	"house": 170_000,
	"car": 25_000,
	"shoes": 90,
	"the shirt off your back": 10,
	"dog": 9999999999999999999999999,
}

d1 = Dealer([],0,"Dealer")
p1 = Player([],0,None,0,starting_items)



# new player state printing
d1.draw(decklist.draw_card())
d1.draw(decklist.draw_card())

p1.draw(decklist.draw_card())
p1.draw(decklist.draw_card())

print(d1)
print(p1)


print()
print("item testing 🡻")
print()

meep = p1.sell_item()
print(meep)
