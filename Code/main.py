# I decided to overhaul main.py
# This runs, but isn't fully functional
# I wasn't happy with our code whatsoever, so I've taken what I've learnt and coded until my brain melted and dribbled out my ears
# I hope this makes sense and is expandable! I think this will be much easier to eventually give a GUI to.
# I have been in the weeds here for a while, so it might be more confusing than I think it is
#   - Nova

from Deck import Deck
from Player import Player
from Dealer import Dealer
from Colors import Colors
from enum import Enum
import os
import time

def main():
# greet user
    print("""\n\n
██████████████████████████████████████████████████████████████████████████████████████████████████████████████ 
██████████████████████████████████████████████████████████████████████████████████████████████████████████████
██                                                                                                          ██
██  ▀█████████▄   ▄█          ▄████████  ▄████████    ▄█   ▄█▄      ▄█    ▄████████  ▄████████    ▄█   ▄█▄  ██
██    ███    ███ ███         ███    ███ ███    ███   ███ ▄███▀     ███   ███    ███ ███    ███   ███ ▄███▀  ██
██    ███    ███ ███         ███    ███ ███    █▀    ███▐██▀       ███   ███    ███ ███    █▀    ███▐██▀    ██
██   ▄███▄▄▄██▀  ███         ███    ███ ███         ▄█████▀        ███   ███    ███ ███         ▄█████▀     ██
██  ▀▀███▀▀▀██▄  ███       ▀███████████ ███        ▀▀█████▄        ███ ▀███████████ ███        ▀▀█████▄     ██
██    ███    ██▄ ███         ███    ███ ███    █▄    ███▐██▄       ███   ███    ███ ███    █▄    ███▐██▄    ██
██    ███    ███ ███▌    ▄   ███    ███ ███    ███   ███ ▀███▄     ███   ███    ███ ███    ███   ███ ▀███▄  ██
██  ▄█████████▀  █████▄▄██   ███    █▀  ████████▀    ███   ▀█▀ █▄ ▄███   ███    █▀  ████████▀    ███   ▀█▀  ██ 
██               ▀                                   ▀         ▀▀▀▀▀▀                            ▀          ██
██                                                                                                          ██
██████████████████████████████████████████████████████████████████████████████████████████████████████████████ 
██████████████████████████████████████████████████████████████████████████████████████████████████████████████ 
""")


# --- INITIALIZATION ---
    minimum_bet = 100
    starting_balance = 100 # it is low like this to show functionality. Increase before releasing
    starting_items = {
        # "house": 50_000,
        # "firstborn": 30_000,
        # "car": 25_000,
        "dog": 666,
        # "watch": 500,
        # "shoes": 90,
        # "pants": 50,
        # "shirt": 15,
        "quit": "exit game"
    }

    # Create players and dealer and sets base wealth to 1000   
    class Clients(Enum): # https://www.geeksforgeeks.org/enum-in-python/
        PLAYER = Player([], 0, None, starting_balance, starting_items)
        CPU1 = Player([], 0, "CPU1", starting_balance, {})
        CPU2 = Player([], 0, "CPU2", starting_balance, {})
        DEALER = Dealer([], 0, "DEALER")

    game_loop(Clients, minimum_bet)
    print("""
  _   _                 _             
 | | | |               | |            
 | |_| |__   __ _ _ __ | | _____      
 | __| '_ \\ / _` | '_ \\| |/ / __|     
 | |_| | | | (_| | | | |   <\\__ \\     
  \\__|_| |_|\\__,_|_| |_|_|\\_\\___/     
  / _|                                
 | |_ ___  _ __                       
 |  _/ _ \\| '__|                      
 | || (_) | |                         
 |_| \\___/|_|         _             _ 
       | |           (_)           | |
  _ __ | | __ _ _   _ _ _ __   __ _| |
 | '_ \\| |/ _` | | | | | '_ \\ / _` | |
 | |_) | | (_| | |_| | | | | | (_| |_|
 | .__/|_|\\__,_|\\__, |_|_| |_|\\__, (_)
 | |             __/ |         __/ |  
 |_|            |___/         |___/   
 """)
    exit()





######################## GAME LOGIC ########################

def game_loop(clients, min_bet):
    # misc variables
    running = True

    while running:
        for c in clients:
            c.value.reset_flags()

        dealer_nat_black = False
        nat_winners = []
        did_bet = False

        print("\n\n-+-+- New round start! -+-+-\n\n")

        # user place bet (and sell if can't meet minimum [and lose if broke])
        while not did_bet:
            bet_outcome = clients.PLAYER.value.bet(min_bet)
            if bet_outcome > 0:
                clients.PLAYER.value.set_player_bet(bet_outcome)
                did_bet = True
            else:
                sale_outcome = clients.PLAYER.value.sell_item()
                if sale_outcome == -1:
                    # no items to sell, game over
                    print("You don't have enough money to continue, and have no items to sell!")
                    print("Game Over!")
                    running = False
                    did_bet = True
                    return
                elif sale_outcome == -2:
                    running = False
                    did_bet = True
                    return
                    


        # add CPU bets
        for c in clients:
            if 'cpu' in c.name.lower():
                c.value.set_player_bet(min_bet)
                c.value.set_player_wealth( c.value.get_player_wealth() - c.value.get_player_bet() )

        # print("DEBUG@game_loop: player bet:",clients.PLAYER.value.get_player_bet()) #DEBUG
        for c in clients:
            if c.name.lower() not in ('dealer'):
                print("DEBUG@game_loop: "+c.name+" bet:",c.value.get_player_bet()) #DEBUG

        # Creates a deck and shuffles the deck
        decklist = Deck([])
        decklist.create_deck()
        decklist.shuffle_deck()
        decklist.shuffle_deck()
        decklist.shuffle_deck()

        # ensure hands are empty, then draw 2 cards to start
        for x in range(2):
            for c in (clients):
                c = c.value
                c.set_hand([])
                c.draw(decklist.draw_card())
                c.draw(decklist.draw_card())

        check_hands(clients)
        display_all_hands(clients)

        # determine if end_round conditions are already met (turn-one blackjack)
        for c in (clients):
            if c.value.get_flags()["natural_blackjack"]:
                if c.name == "DEALER":
                    print("DEBUG:: !!!DEALER!!!: NAT BLACKJACK")
                    dealer_nat_black = True
                else:
                    print("DEBUG: "+str(c.name)+": NAT BLACKJACK")
                    c.value.set_flag("natural_blackjack", True)
                    nat_winners.append(c.name)

        # if a player does have nat blackjack, check the dealer;   if both have nat black, player pushes
        if nat_winners != [] and dealer_nat_black:
            print("DEBUG: dealer+player natural_blackjack; push for player")
            for name in nat_winners:
                clients.name.set_flag("push", True)

        # player wins with nat blackjack
        if len(nat_winners) == 1 and not dealer_nat_black:
            bet_resolution(clients)

        # no nat blackjacks to end game with: player continues to 'Hit, Stand, or Bust'
        c_flag = clients.PLAYER.value.get_flags()
        while not c_flag["bust"] and not c_flag["finished_turn"]:
            c_decision = hit_stand(clients.PLAYER)
            if c_decision == 'hit':
                clients.PLAYER.value.draw(decklist.draw_card())
                check_hands(clients)
                print(clients.PLAYER.value)
            else:
                clients.PLAYER.value.set_flag('finished_turn', True)
            # update flags for next iteration
            check_hands(clients)
            c_flag = clients.PLAYER.value.get_flags()

        # after player is done, let CPU and Dealer play
        cpu_resolve(clients, decklist)

        # end-of-round display, dealer flips hole card
        check_hands(clients)
        display_all_hands(clients, hide_hole=False)
        # victory_check(clients)

def victory_check(clients):
#Winning the Game
    # Blackjack: 
        # If your first two cards are an Ace and a 10-value card (10, Jack, Queen, King), 
        # this is an automatic win (Blackjack) and pays out at a higher rate than a regular win (usually ×1.5).
    # Higher Value than Dealer: 
        # If your hand total is closer to 21 than the dealer’s hand total without going bust, you win. 
        # Winnings are typically paid out at 1:1.
    # Dealer Busts: 
        # If the dealer’s hand total goes over 21 (busts), you win regardless of your hand value.
    # Push: 
        # If your hand total equals the dealer’s hand total, 
        # it’s a tie (push) and your bet is returned without any winnings or losses.
    # Lower Value than Dealer: 
        # If the dealer’s hand total is closer to 21 than yours without busting, you lose your bet.

    outcome_txt = ""

    dealer_flags = clients.DEALER.value.get_flags()
    if dealer_flags['bust']:
        outcome_txt += "Dealer bust! Players reign supreme!"
        for c in clients:
            if c.name in ('player', 'cpu'):
                print("DEBUG@victory_check(): "+c.name+" check")
                if not c.value.get_flags()['bust']:
                    wealth = c.value.get_player_wealth()
                    bet = c.value.get_player_bet()
                    c.value.set_player_wealth(wealth + (bet*2))


    # Lose – the player’s bet is taken by the dealer.
    # Win – the player wins as much as they bet. If you bet $10, you win $10 from the dealer (plus you keep your original bet, of course.)
    # Blackjack (natural) – the player wins 1.5 times the bet. With a bet of $10, you keep your $10 and win a further $15 from the dealer.
    # Push – the hand is a draw. The player keeps their bet, neither winning nor losing money.




def cpu_resolve(clients, decklist):
    # rules for CPU and Dealer drawing
        # Dealer Hits: The dealer is required to draw if they have a hand of less than 17. 
        # Dealer Stands: The dealer is required to stand with 17 and more in their hand. 
    check_hands(clients)
    for c in (clients):
        if "player" not in c.name.lower():
            print("DEBUG@cpu_resolve(): CPU play!",c.name)
            while c.value.get_hand_value() < 17:
                c.value.draw(decklist.draw_card())
            c.value.set_flag('finished_turn', True)



def dealer_resolve(d):
    pass




def hit_stand(c):
    # gets user decision for hitting or standing
    valid_choice = False
    while not valid_choice:
        try:
            choice = str(input( (str(c.name)+" > Hit or stand? :") ))
            if choice.lower() in ('h','hit'):
                print(str(c.name) + " hits...")
                choice = 'hit'
                valid_choice = True
            elif choice.lower() in ('s', 'stand'):
                print(str(c.name) + " stands...")
                choice = 'stand'
                valid_choice = True
            else:
                print(Colors.red+"Please enter a valid input ('h','hit','s','stand')"+Colors.reset)
        except KeyboardInterrupt:
            print(Colors.red+"quitting..."+Colors.reset)
            exit()
        except BaseException as e:
            print(e) #DEBUG
            print(Colors.red+"Ya broke it! Try again."+Colors.reset)

    if choice == 'hit':
        return "hit"
    else:            
        return "stand"



    # user choice to hit or stand

def bet_resolution(clients):
    # method for resolving bets after a round has ended
    # TODO
    pass

def end_round(clients, decklist):
    # after all players have finished their turn, dealer follows drawing rules
    # TODO
    print("DEBUG@final_turn():") #DEBUG


def check_for_win(clients):
    for c in (clients):
        if c.name == "DEALER" and c.value.get_flags()["bust"]:
            print("*"*20,"DEALER BUST","*"*20)

def display_all_hands(clients, hide_hole=True):
    print()
    time.sleep(0.5)
    for c in (clients):
        if c.name == "DEALER":
            c.value.set_flag("hide_hole", hide_hole)
        print("DEBUG@display_all_hands(): "+c.name,str(c.value.get_flags())) #DEBUG
        print(c.value)
        time.sleep(0.1)

def check_hands(clients):
    # print("\t\tDEBUG@check_hands(): START CHECK")
    for c in clients:
        # print("\nDEBUG@check_hands(): client:"+c.name)
        c = c.value

        if c.get_flags()["bust"]:
            # print("DEBUG@check_hands(): bust is true, skipping...")
            continue

        val = c.get_hand_value()

        if val > 21:
            c.set_flag("bust", True)
        elif val == 21 and len(c.get_hand()) == 2: 
            c.set_flag("natural_blackjack", True)
        elif val == 21: 
            c.set_flag("blackjack", True)


if __name__ == '__main__':
    main()