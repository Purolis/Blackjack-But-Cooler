# testing to make sure my changes work and don't cause a Chernobyl-esque disaster

from Deck import Deck
from Player import Player
from Dealer import Dealer
from Card import Card
from Colors import Colors
from enum import Enum
import re
import sys
import os
import time

# the tests listed highlight functionality in the changes I made

def main(mode="cli"):
	print("mode: " + str(mode))

	running = True
	while running:
		choice = str(input("""
test menu:
1) toString
2) item
3) bet
4) ace reduction
5) flag printing
x) exit

:"""))
		match(choice):
			case "1":
				print("toString test!"+("-"*10)+"\n\n")
				toString_test()
			case "2":
				print("item test!"+("-"*10)+"\n\n")
				item_test()
			case "3":
				print("item test!"+("-"*10)+"\n\n")
				bet_test()
			case "4":
				print("ace reduction test!"+("-"*10)+"\n\n")
				ace_reduction()
			case "5":
				print("flag print test!"+("-"*10)+"\n\n")
				flag_printing()
			case _:
				print("exiting...\n")
				running = False
	exit()


def flag_printing():
	decklist = Deck([])
	decklist.create_deck()
	decklist.shuffle_deck()

	minimum_bet = 100
	starting_balance = 300
	bet_pool = {} # <client>: <bet_amnt>

	starting_items = {
		"house": 50_000,
		"firstborn": 30_000,
		"car": 25_000,
		"dog": 666,
		"watch": 500,
		"shoes": 90,
		"pants": 50,
		"shirt": 15,
    }

    # Create players and dealer and sets base wealth to 1000   
	class Clients(Enum): 
		PLAYER = Player([], 0, None, starting_balance, starting_items)
		NAT_BKJK = Player([], 0, "NAT_BKJK", starting_balance, {})
		BLK_JK = Player([], 0, "BLK_JK", starting_balance, {})
		OUT = Player([], 0, "OUT", 0, {})
		BUST = Player([], 0, "BUST", starting_balance, {})
		PSH = Player([], 0, "PSH", starting_balance, {}) # this one is just for 'push' flag testing (set arbitrarily)
		DEALER1 = Dealer([], 0, "DEALER_hide")
		DEALER2 = Dealer([], 0, "DEALER_show")

	for i in range(3):
		Clients.PLAYER.value.draw(decklist.draw_card())
	Clients.NAT_BKJK.value.set_hand([
		Card(11, 'Diamonds', 'Ace of Diamonds'), 
		Card(10, 'Diamonds', 'Queen of Diamonds'), 
		])
	Clients.BLK_JK.value.set_hand([
		Card(11, 'Diamonds', 'Ace of Diamonds'), 
		Card(10, 'Diamonds', 'Queen of Diamonds'), 
		Card(10, 'Hearts', 'King of Hearts'), 
		])
	Clients.BUST.value.set_hand([
		Card(11, 'Diamonds', 'Ace of Diamonds'), 
		Card(11, 'Hearts', 'Ace of Hearts'), 
		Card(10, 'Diamonds', 'Queen of Diamonds'), 
		Card(10, 'Diamonds', 'Jack of Diamonds'), 
		])
	Clients.PSH.value.set_hand([
		Card(5, 'Diamonds', '5 of Diamonds'), 
		Card(8, 'Diamonds', '8 of Diamonds'), 
		])
	Clients.DEALER1.value.set_hand([
		Card(2, 'Diamonds', '2 of Diamonds'), 
		Card(8, 'Diamonds', '8 of Diamonds'),  
		])
	Clients.DEALER2.value.set_hand([
		Card(5, 'Diamonds', '5 of Diamonds'), 
		Card(8, 'Diamonds', '8 of Diamonds'), 
		])

	check_hands(Clients)
	Clients.OUT.value.set_flag('out_of_game', True)

	display_all_hands(Clients)

	Clients.DEALER1.value.set_flag('hide_hole', True)
	Clients.DEALER2.value.set_flag('hide_hole', False)
	print(Clients.DEALER1.value)
	print(Clients.DEALER2.value)

	
def ace_reduction():
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

	d1 = Dealer([],0,"DEALER")
	user = Player([],0,None,200,starting_items) 

	user.set_hand([
		Card(11, 'Diamonds', 'Ace of Diamonds'), 
		Card(10, 'Diamonds', 'King of Diamonds'), 
		Card(10, 'Hearts', 'Queen of Hearts'),
	])

	d1.set_hand([
		Card(11, 'Diamonds', 'Ace of Diamonds'), 
		Card(11, 'Clubs', 'Ace of Clubs'), 
		Card(11, 'Spades', 'Ace of Spades'), 
	])
	
	print(user)
	print(d1)

def bet_test():
	d1 = Dealer([],0,"DEALER")
	user = Player([],0,None,200,{"foo":10}) 
	user.bet()

def toString_test():
	#NOTE: this does not handle flags, so there are slight differences (no conditional text output)
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

	d1 = Dealer([],0,"DEALER")
	d2 = Dealer([],0,"d2")
	user = Player([],0,None,200,starting_items) 
		# name=None 🡸 this indicates that this instance of 'Player' is the person behind the keyboard.
		# 	this highlights the player's state in a different color to make it easier to understand at a glance.

	d1.draw(decklist.draw_card())
	d1.draw(decklist.draw_card())
	d2.draw(decklist.draw_card())
	d2.draw(decklist.draw_card())
	user.draw(decklist.draw_card())
	user.draw(decklist.draw_card())
	print()
	print(d1)
	print(d2)
	print(user)

def item_test():
	starting_items = {
		"house": 170_000,
		"car": 25_000,
		"shoes": 90,
		"shirt": 10,
		"dog": 300,
	}

	user = Player([],0,None,200,starting_items) 

	# new: item selling as class method
	print("item testing 🡻")
	print()

	run = True
	while run:
		user.sell_item()
		choice = input("continue? [y/N]: ")
		match(choice.lower()):
			case "y":
				continue
			case _:
				run = False

def check_hands(clients):
    print("\t\tDEBUG@check_hands(): START CHECK")
    for c in clients:
        print("\nDEBUG@check_hands(): client:"+c.name)
        c = c.value

        if c.get_flags()["out_of_game"]:
        	print("MEEP")
        elif c.get_flags()["bust"]:
            print("DEBUG@check_hands(): bust is true, skipping...")
        else:
	        val = c.get_hand_value()
	        if val > 21:
	            c.set_flag("bust", True)
	        elif val == 21 and len(c.get_hand()) == 2: 
	            c.set_flag("natural_blackjack", True)
	        elif val == 21: 
	            c.set_flag("blackjack", True)

def display_all_hands(clients, hide_hole=True):
    print()
    time.sleep(0.5)
    for c in (clients):
        if re.search("DEALER|PLAYER", c.name):
            continue
        # print("DEBUG@display_all_hands(): "+c.name,str(c.value.get_flags())) #DEBUG
        print(c.value)
        time.sleep(0.1)

    print(clients.PLAYER.value)
    time.sleep(0.1)

if __name__ == '__main__':
	# take in command-line arguments, launch as CLI or GUI
	if len(sys.argv) > 1:
		mode = str(sys.argv[1])
		if mode in ['-gui', '-GUI', '--graphic']:
			mode = "gui"
		main(mode)
	else:
		main()