from Deck import Deck
from Player import Player
from Dealer import Dealer
import os
import time
import sys

# testing to make sure my changes work and don't cause a Chernobyl-esque disaster
# this highlights the changes I made
# main.py WILL have to be refactored quite heavily, I realize, but I believe this is a better direction
	# that will help massively with the readability of our code.


def main(mode="cli"):
	print("mode: " + str(mode))

	running = True
	while running:
		choice = str(input("""
test menu:
1) toString test
2) item test
x) exit

:"""))
		match(choice):
			case "1":
				print("toString test!"+("-"*10)+"\n\n")
				toString_test()
			case "2":
				print("item test!"+("-"*10)+"\n\n")
				item_test()
			case _:
				print("exiting...\n")
				running = False
	exit()

	


	

def toString_test():
	decklist = Deck([])
	decklist.create_deck()
	decklist.shuffle_deck()

	starting_items = {
		"house": 170_000,
		"car": 25_000,
		"shoes": 90,
		"the shirt off your back": 10,
		"dog": 300,
	}

	d1 = Dealer([],0,"Dealer")
	user = Player([],0,None,200,starting_items) 
		# name=None 🡸 this indicates that this instance of 'Player' is the person behind the keyboard.
		# 	this highlights the player's state in a different color to make it easier to understand at a glance.

	# new: player state printing
	d1.draw(decklist.draw_card())
	d1.draw(decklist.draw_card())

	user.draw(decklist.draw_card())
	user.draw(decklist.draw_card())

	print()
	print(d1)
	print(user)


def item_test():
	starting_items = {
		"house": 170_000,
		"car": 25_000,
		"shoes": 90,
		"the shirt off your back": 10,
		"dog": 300,
	}

	user = Player([],0,None,200,starting_items) 

	# new: item selling as class method
	print("item testing 🡻")
	print()

	user.sell_item()


if __name__ == '__main__':
	# take in command-line arguments, launch as CLI or GUI
	if len(sys.argv) > 1:
		mode = str(sys.argv[1])
		if mode in ['-gui', '-GUI', '--graphic']:
			mode = "gui"
		main(mode)
	else:
		main()